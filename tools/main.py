#!/usr/bin/env python3
"""
自動技術調査スクリプト
arXivのRSSフィードから最新の情報科学論文を取得し、Gemini APIで解析する
"""

import argparse
from collections import defaultdict
import time
import yaml
import os
from analyzer import GeminiAnalyzer
from fetchers import ArxivRSSFetcher
from fetchers import HuggingFaceFetcher
from paper_tracker import PaperTracker
from slack_notifier import SlackNotifier
from utils import save_summary

# Configuration will be loaded from YAML file
config = {}


def load_config(config_path):
    """YAMLファイルから設定を読み込む"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def parse_args():
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(description="自動技術調査スクリプト")
    parser.add_argument(
        '-s', '--source',
        choices=['a', 'h'],
        default='h',
        help="論文の取得元を指定 (a: arXiv, h: Hugging Face Daily Papers)"
    )
    parser.add_argument(
        '-c', '--config',
        default='config/base.yaml',
        help="設定ファイルのパス (デフォルト: config/base.yaml)"
    )
    return parser.parse_args()


def clearup_old_summaries(tracker: PaperTracker, days: int = 7) -> None:
    """
    指定した日数より古い要約ファイルを削除する

    Args:
        tracker: PaperTrackerインスタンス
        days: 削除対象の日数（デフォルト7日）

    """
    print(f"\n{days}日経過した古い要約ファイルを削除中...")
    deleted_files = tracker.cleanup_old_summaries(days=days)
    if deleted_files:
        print(f"{len(deleted_files)}件の古い要約ファイルを削除しました")
    else:
        print("削除対象の古いファイルはありませんでした")


def main():
    args = parse_args()
    
    # Load configuration
    global config
    config_path = os.path.join(os.path.dirname(__file__), args.config)
    config = load_config(config_path)
    
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        print("エラー: 環境変数 GEMINI_API_KEY が設定されていません")
        return

    SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
    if not SLACK_WEBHOOK_URL:
        print("警告: 環境変数 SLACK_WEBHOOK_URL が設定されていません")
        slack_notifier = None
    else:
        slack_notifier = SlackNotifier(SLACK_WEBHOOK_URL)

    print(f"=== 自動技術調査スクリプト ===")
    print(f"論文ソース: {'arXiv' if args.source == 'a' else 'Hugging Face Daily Papers'}")

    if args.source == 'a':
        print(f"カテゴリ: {', '.join(config['arxiv']['categories'])}")
        print(f"カテゴリごとの最大論文数: {config['arxiv']['max_papers_per_category']}")
    else:
        print(f"全体の最大論文数: {config['hugging_face']['max_papers']}")

    tracker = PaperTracker()
    all_papers = []

    if args.source == 'a':
        fetcher = ArxivRSSFetcher()
        for category in config['arxiv']['categories']:
            print(f"\nカテゴリ {category} から論文を取得中...")
            papers = fetcher.fetch_papers(category=category, max_results=config['arxiv']['max_papers_per_category'] * 2)  # 余裕を持って2倍取得
            all_papers.extend(papers)
        # サンプル実行用のダミーデータ（テスト用）
        # all_papers = [
        #     Paper(
        #         arxiv_id="2303.12077",
        #         title="VAD: Vectorized Scene Representation for Efficient Autonomous Driving",
        #         authors="Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, Xinggang Wang",
        #         abstract="Autonomous driving requires a comprehensive understanding of the surrounding environment for reliable trajectory planning. Previous works rely on dense rasterized scene representation (e.g., agent occupancy and semantic map) to perform planning, which is computationally intensive and misses the instance-level structure information. In this paper, we propose VAD, an end-to-end vectorized paradigm for autonomous driving, which models the driving scene as a fully vectorized representation. The proposed vectorized paradigm has two significant advantages. On one hand, VAD exploits the vectorized agent motion and map elements as explicit instance-level planning constraints which effectively improves planning safety. On the other hand, VAD runs much faster than previous end-to-end planning methods by getting rid of computation-intensive rasterized representation and hand-designed post-processing steps. VAD achieves state-of-the-art end-to-end planning performance on the nuScenes dataset, outperforming the previous best method by a large margin. Our base model, VAD-Base, greatly reduces the average collision rate by 29.0% and runs 2.5x faster. Besides, a lightweight variant, VAD-Tiny, greatly improves the inference speed (up to 9.3x) while achieving comparable planning performance. We believe the excellent performance and the high efficiency of VAD are critical for the real-world deployment of an autonomous driving system. Code and models are available at this https URL for facilitating future research.",
        #         categories="cs.RO",
        #         published="2023-03-21",
        #         link="https://arxiv.org/abs/2303.12077",
        #         pdf_link="https://arxiv.org/pdf/2303.12077.pdf"
        #     )
        # ]
    elif args.source == 'h':
        print("Hugging Face Daily Papersから論文を取得中...")
        hf_fetcher = HuggingFaceFetcher()
        all_papers = hf_fetcher.fetch_papers(max_papers=config['hugging_face']['max_papers'])

    if not all_papers:
        print("論文が取得できませんでした")
        clearup_old_summaries(tracker)
        return

    # 未要約の論文のみをフィルタリング
    new_papers = []

    if args.source == 'a':
        # arXivの場合：カテゴリごとに最大ARXIV_MAX_PAPERS_PER_CATEGORYつまで
        category_counts = defaultdict(int)
        for paper in all_papers:
            if not tracker.is_summarized(paper.link):
                # 論文のカテゴリを取得（複数カテゴリの場合は最初のものを使用）
                paper_category = paper.categories.split(',')[0].strip() if hasattr(paper, 'categories') and paper.categories else paper.category

                # カテゴリごとのカウントを管理
                if category_counts[paper_category] < config['arxiv']['max_papers_per_category']:
                    new_papers.append(paper)
                    category_counts[paper_category] += 1
    else:
        for paper in all_papers:
            if not tracker.is_summarized(paper.link):
                new_papers.append(paper)
                if len(new_papers) >= config['hugging_face']['max_papers']:
                    break

    if not new_papers:
        print("新しい論文が見つかりませんでした")
        clearup_old_summaries(tracker)
        return

    papers = new_papers
    if args.source == 'a':
        print(f"新しい論文を{len(papers)}件発見しました（カテゴリごとに最大{config['arxiv']['max_papers_per_category']}件）")
    else:
        print(f"新しい論文を{len(papers)}件発見しました")

    # 2. Gemini API で論文を解析
    print("\nGemini APIで論文を解析中...")
    analyzer = GeminiAnalyzer(GEMINI_API_KEY)

    for i, paper in enumerate(papers, 1):
        print(f"\n処理中 [{i}/{len(papers)}]: {paper.title}")

        # 論文を解析
        summary = analyzer.analyze_paper(paper)
        file_path = save_summary(paper, summary)
        tracker.add_summarized_paper(paper, file_path)

        # Slackに通知を送信
        if slack_notifier:
            slack_notifier.send_notification(paper, summary)

        # API レート制限対策
        if i < len(papers):
            time.sleep(1)

    print(f"\n調査が完了しました！")
    print(f"これまでに要約した論文の総数: {tracker.get_summary_count()}件")

    # 一時PDFファイルを削除
    analyzer.pdf_processor.cleanup_temp_files()
    clearup_old_summaries(tracker)


if __name__ == "__main__":
    main()