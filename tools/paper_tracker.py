"""
論文の要約状況を追跡するためのモジュール
要約済みの論文URLをCSVファイルで管理
"""

import csv
import os
from datetime import datetime, timedelta
from typing import Set, List, Optional


class PaperTracker:
    """要約済み論文を追跡するクラス"""

    def __init__(self, csv_path: str = "../summarized_papers.csv"):
        """
        初期化

        Args:
            csv_path: 追跡用CSVファイルのパス
        """
        self.csv_path = csv_path
        self._ensure_csv_exists()

    def _ensure_csv_exists(self):
        """CSVファイルが存在しない場合は作成"""
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['url', 'arxiv_id', 'title', 'summarized_at', 'file_path'])

    def is_summarized(self, url: str) -> bool:
        """
        指定されたURLの論文が既に要約済みかチェック

        Args:
            url: 論文のURL

        Returns:
            要約済みならTrue
        """
        summarized_urls = self.get_summarized_urls()
        return url in summarized_urls

    def get_summarized_urls(self) -> Set[str]:
        """
        要約済み論文のURLセットを取得

        Returns:
            要約済み論文のURLのセット
        """
        urls = set()
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'url' in row:
                        urls.add(row['url'])
        except FileNotFoundError:
            self._ensure_csv_exists()
        return urls

    def add_summarized_paper(self, paper, file_path: Optional[str] = None):
        """
        要約済み論文を記録

        Args:
            paper: Paperオブジェクト
            file_path: 要約ファイルのパス
        """
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                paper.link,
                paper.arxiv_id,
                paper.title,
                datetime.now().isoformat(),
                file_path or ""
            ])

    def get_summary_count(self) -> int:
        """
        要約済み論文の総数を取得

        Returns:
            要約済み論文の数
        """
        return len(self.get_summarized_urls())
    
    def cleanup_old_summaries(self, days: int = 7) -> List[str]:
        """
        指定した日数より古い要約ファイルを削除する
        
        Args:
            days: 削除対象とする日数（デフォルト: 7日）
            
        Returns:
            削除されたファイルパスのリスト
        """
        deleted_files = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        try:
            # 既存のレコードを読み込み
            rows_to_keep = []
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # 要約日時をパース
                        summarized_at = datetime.fromisoformat(row['summarized_at'])
                        
                        if summarized_at < cutoff_date:
                            # 古いファイルを削除
                            file_path = row.get('file_path', '')
                            if file_path and os.path.exists(file_path):
                                os.remove(file_path)
                                deleted_files.append(file_path)
                                print(f"削除済み: {file_path}")
                        else:
                            # 新しいレコードは保持
                            rows_to_keep.append(row)
                    except (ValueError, KeyError) as e:
                        print(f"レコードの処理中にエラー: {e}")
                        # エラーがあるレコードも保持
                        rows_to_keep.append(row)
            
            # CSVファイルを更新（古いレコードを削除）
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                if rows_to_keep:
                    fieldnames = rows_to_keep[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows_to_keep)
                else:
                    # レコードがない場合はヘッダーのみ書き込み
                    writer = csv.writer(f)
                    writer.writerow(['url', 'arxiv_id', 'title', 'summarized_at', 'file_path'])
                    
        except FileNotFoundError:
            print(f"CSVファイルが見つかりません: {self.csv_path}")
        except Exception as e:
            print(f"古いファイルの削除中にエラーが発生しました: {e}")
            
        return deleted_files