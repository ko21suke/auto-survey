"""ユーティリティ関数"""
import os
import re
from datetime import datetime
from paper import Paper


def save_summary(paper: Paper, summary: str, output_dir: str = "../summary") -> str:
    """
    論文の要約をMarkdownファイルとして保存

    Args:
        paper: 論文情報
        summary: 生成された要約
        output_dir: 保存先ディレクトリ

    Returns:
        保存されたファイルのパス
    """
    # ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)

    # ファイル名を論文タイトルから生成（特殊文字を除去）
    safe_title = re.sub(r'[<>:"/\\|?*]', '', paper.title)
    safe_title = safe_title.replace('\n', ' ').strip()
    filename = f"{safe_title}.md"
    filepath = os.path.join(output_dir, filename)

    # Markdownファイルの内容を作成
    content = f"""# {paper.title}

**arXiv ID**: [{paper.arxiv_id}]({paper.link})
**PDF**: [ダウンロード]({paper.pdf_link})
**著者**: {paper.authors}
**カテゴリ**: {paper.categories}
**公開日**: {paper.published}

---

## 要約

{summary}

---

*このファイルは自動生成されました。生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*
"""

    # ファイルに保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n要約を保存しました: {filepath}")

    return filepath