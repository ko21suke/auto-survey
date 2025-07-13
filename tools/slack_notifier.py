"""Slack通知を処理するモジュール"""
import requests
from paper import Paper


class SlackNotifier:
    """Slackへの通知を処理するクラス"""

    def __init__(self, webhook_url: str):
        """
        Args:
            webhook_url: SlackのWebhook URL
        """
        self.webhook_url = webhook_url

    def summarize_for_slack(self, paper: Paper, full_summary: str, max_chars: int = 500) -> str:
        """
        論文の要約から#0short_summaryセクションを抽出

        Args:
            paper: 論文情報
            full_summary: Geminiによる完全な要約
            max_chars: 最大文字数（デフォルト200）

        Returns:
            #0short_summaryセクションの内容
        """
        # #0short_summaryセクションから情報を抽出
        lines = full_summary.split('\n')
        summary_section = []
        in_short_summary = False

        for line in lines:
            if 'ショートサマリ' in line or 'short_summary' in line:
                in_short_summary = True
                continue
            elif line.startswith('##') and in_short_summary:
                break
            elif in_short_summary and line.strip():
                summary_section.append(line.strip())

        # #0short_summaryセクションが見つからない場合はアブストラクトを使用
        if not summary_section:
            base_text = paper.abstract
        else:
            base_text = ' '.join(summary_section)

        # テキストを短縮（必要に応じて）
        if len(base_text) > max_chars:
            # 文の区切りで切る
            sentences = base_text.replace('。', '。\n').split('\n')
            shortened = ""
            for sentence in sentences:
                if len(shortened) + len(sentence) <= max_chars - 3:
                    shortened += sentence
                else:
                    if shortened:
                        shortened += "..."
                    break
            return shortened or base_text[:max_chars-3] + "..."

        return base_text

    def create_slack_message(self, paper: Paper, short_summary: str) -> dict:
        """
        Slack用のメッセージを作成

        Args:
            paper: 論文情報
            short_summary: 短縮版の要約

        Returns:
            Slack API用のメッセージ辞書
        """
        # 4つの箇条書きポイントを作成
        bullet_points = []

        # 1. 論文の基本情報
        bullet_points.append(f"📄 *{paper.title}*")

        # 2. カテゴリとarXiv ID
        bullet_points.append(f"🏷️ カテゴリ: {paper.categories} | arXiv: {paper.arxiv_id}")

        # 3. PDFリンク
        bullet_points.append(f"📖 <{paper.pdf_link}|PDFを見る>")

        # 4. 要約ファイルの場所
        bullet_points.append(f"💾 詳細な要約が `summary/{paper.title}.md` に保存されました")

        # Slackメッセージの構築
        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🚚 新しい論文情報をお届け",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "\n".join([f"• {point}" for point in bullet_points])
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*要約:*\n{short_summary}"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"公開日: {paper.published}"
                        }
                    ]
                }
            ]
        }

        return message

    def send_notification(self, paper: Paper, summary: str) -> bool:
        """
        Slackに論文の要約を送信

        Args:
            paper: 論文情報
            summary: Geminiによる要約

        Returns:
            送信成功時True、失敗時False
        """
        try:
            # 要約を短縮
            short_summary = self.summarize_for_slack(paper, summary)

            # Slackメッセージを作成
            message = self.create_slack_message(paper, short_summary)

            # Webhookに送信
            response = requests.post(
                self.webhook_url,
                json=message,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print(f"✅ Slackに通知を送信しました: {paper.title[:50]}...")
                return True
            else:
                print(f"❌ Slack通知の送信に失敗しました: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Slack通知中にエラーが発生しました: {e}")
            return False