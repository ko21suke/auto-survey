"""
Hugging Face Daily Papersから論文を取得するモジュール
"""

import re
import requests
from bs4 import BeautifulSoup
import feedparser
from typing import List
from fetchers.base import Fetcher
from paper import Paper


class HuggingFaceFetcher(Fetcher):
    """Hugging Face Daily Papersから論文を取得するクラス"""

    def __init__(self):
        super().__init__()
        self.rss_url = "https://granary.io/url?input=jsonfeed&output=rss&url=https://jamesg.blog/hf-papers.json"

    def fetch_papers(self, **kwargs) -> List[Paper]:
        """
        Hugging Face Daily Papersから論文を取得

        Args:
            **kwargs: オプションの引数
                max_papers (int): 取得する論文の最大数（デフォルト: 5）

        Returns:
            List[Paper]: 取得した論文のリスト
        """
        max_papers = kwargs.get('max_papers', 5)
        return self.fetch_top_papers(max_papers)

    def fetch_top_papers(self, max_papers=5):
        """
        Hugging Face Daily Papersの上位論文を取得（upvote数順）

        Args:
            max_papers (int): 取得する論文の最大数

        Returns:
            list[Paper]: 取得した論文のリスト
        """
        print(f"Hugging Face RSSフィードを取得中: {self.rss_url}")
        feed = self.parse_feed(self.rss_url)

        if not feed.entries:
            print("RSSフィードから論文を取得できませんでした")
            return []

        # 各論文のupvote数を取得
        papers_with_upvotes = []
        print(f"\n{len(feed.entries)}件の論文からupvote数を取得中...")

        for i, entry in enumerate(feed.entries):
            try:
                hf_link = entry.get('link', '')
                if 'huggingface.co/papers/' in hf_link:
                    # Hugging Faceページからupvote数を取得
                    upvotes = self._get_upvotes(hf_link)
                    if upvotes is not None:
                        papers_with_upvotes.append((entry, upvotes))
                        print(f"[{i+1}/{len(feed.entries)}] {entry.title[:50]}... - {upvotes} upvotes")
            except Exception as e:
                print(f"upvote数取得エラー: {e}")
                continue

        # upvote数でソート（降順）
        papers_with_upvotes.sort(key=lambda x: x[1], reverse=True)
        print(f"\n上位{max_papers}件の論文を処理中...")

        papers = []
        for i, (entry, upvotes) in enumerate(papers_with_upvotes[:max_papers]):
            try:
                print(f"\n[{i+1}/{max_papers}] 処理中: {entry.title} ({upvotes} upvotes)")

                # エントリからarXiv IDを抽出（親クラスのメソッドを使用）
                arxiv_id = self._extract_arxiv_id_from_entry(entry)
                if not arxiv_id:
                    print(f"arXiv IDを抽出できませんでした: {entry.title}")
                    continue

                # arXivから論文情報を取得
                paper = self._fetch_arxiv_paper(arxiv_id, entry)
                if paper:
                    papers.append(paper)
                    print(f"✓ 論文を取得: {paper.title}")

            except Exception as e:
                print(f"論文の処理中にエラーが発生しました: {e}")
                continue

        return papers

    def _extract_arxiv_id_from_entry(self, entry):
        """
        RSSエントリからarXiv IDを抽出

        Args:
            entry: RSSフィードのエントリ

        Returns:
            str: arXiv ID（見つからない場合はNone）
        """
        # 複数の場所からarXiv IDを探す
        search_texts = []

        # タイトル、リンク、説明文を検索対象に追加
        if hasattr(entry, 'title'):
            search_texts.append(entry.title)
        if hasattr(entry, 'link'):
            search_texts.append(entry.link)
        if hasattr(entry, 'description'):
            search_texts.append(entry.description)
        if hasattr(entry, 'summary'):
            search_texts.append(entry.summary)

        # arXiv IDのパターンを探す（親クラスのメソッドを使用）
        for text in search_texts:
            arxiv_id = self.extract_arxiv_id(text)
            if arxiv_id:
                return arxiv_id

        # Hugging Faceのリンクから直接取得を試みる
        if hasattr(entry, 'link') and 'huggingface.co' in entry.link:
            arxiv_id = self._scrape_arxiv_id_from_hf(entry.link)
            if arxiv_id:
                return arxiv_id

        return None

    def _scrape_arxiv_id_from_hf(self, hf_url):
        """
        Hugging FaceのページからarXiv IDをスクレイピング

        Args:
            hf_url (str): Hugging FaceのページURL

        Returns:
            str: arXiv ID（見つからない場合はNone）
        """
        try:
            response = requests.get(hf_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # arXivリンクを探す
                arxiv_links = soup.find_all('a', href=re.compile(r'arxiv\.org'))
                for link in arxiv_links:
                    href = link.get('href')
                    match = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', href)
                    if match:
                        return match.group(1)

                # ページ内のテキストからも探す
                page_text = soup.get_text()
                match = re.search(r'arXiv:(\d{4}\.\d{4,5})', page_text)
                if match:
                    return match.group(1)

        except Exception as e:
            print(f"Hugging Faceページのスクレイピング中にエラー: {e}")

        return None

    def _get_upvotes(self, hf_url):
        """
        Hugging FaceのページからUpvote数を取得

        Args:
            hf_url (str): Hugging Faceの論文ページURL

        Returns:
            int: upvote数（取得失敗時はNone）
        """
        try:
            response = requests.get(hf_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # upvote数を探す - Hugging Faceの実際のHTML構造に基づく
                # パターン1: label要素内のUpvoteテキストとその隣の数値
                import re
                labels = soup.find_all('label')
                for label in labels:
                    text = label.get_text().strip()
                    if 'Upvote' in text:
                        # Upvoteの後の数値を探す
                        match = re.search(r'Upvote\s*(\d+)', text)
                        if match:
                            return int(match.group(1))

                        # または、div要素内のtext-orange-500クラスを持つ要素を探す
                        orange_divs = label.find_all('div', {'class': lambda x: x and 'text-orange-500' in x if x else False})
                        for div in orange_divs:
                            try:
                                return int(div.get_text().strip())
                            except:
                                pass

                # パターン2: UpvoteControlコンポーネント内の数値を探す
                upvote_controls = soup.find_all('div', {'data-target': 'UpvoteControl'})
                for control in upvote_controls:
                    text = control.get_text()
                    match = re.search(r'Upvote\s*(\d+)', text)
                    if match:
                        return int(match.group(1))

                # パターン3: data-props内のupvotes値を探す
                import json
                for elem in soup.find_all(attrs={'data-props': True}):
                    try:
                        props = json.loads(elem['data-props'])
                        if 'upvotes' in props:
                            return int(props['upvotes'])
                    except:
                        pass

                # 見つからない場合は0を返す
                return 0

        except Exception as e:
            print(f"Upvote数取得エラー ({hf_url}): {e}")
            return None

    def _fetch_arxiv_paper(self, arxiv_id, hf_entry):
        """
        arXiv IDから論文情報を取得

        Args:
            arxiv_id (str): arXiv ID
            hf_entry: Hugging Faceのエントリ（追加情報用）

        Returns:
            Paper: 論文オブジェクト（失敗時はNone）
        """
        try:
            # arXiv APIを使用して論文情報を取得
            api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
            response = requests.get(api_url, timeout=10)

            if response.status_code != 200:
                print(f"arXiv APIエラー: {response.status_code}")
                return None

            # XMLをパース
            feed = feedparser.parse(response.text)

            if not feed.entries:
                print(f"arXiv ID {arxiv_id} の論文が見つかりませんでした")
                return None

            entry = feed.entries[0]

            # 著者リストを整形
            authors = []
            if hasattr(entry, 'authors'):
                authors = [author.name for author in entry.authors]

            # カテゴリを取得
            categories = []
            if hasattr(entry, 'tags'):
                categories = [tag.term for tag in entry.tags]

            # Paperオブジェクトを作成（親クラスのメソッドを使用）
            paper = self.create_paper(
                arxiv_id=arxiv_id,
                title=entry.title.replace('\n', ' ').strip(),
                authors=", ".join(authors),
                abstract=entry.summary.replace('\n', ' ').strip(),
                categories=", ".join(categories) if categories else "cs.LG",  # デフォルトカテゴリ
                published=entry.published,
                link=entry.link,
                pdf_link=entry.link.replace('/abs/', '/pdf/') + '.pdf'
            )

            return paper

        except Exception as e:
            print(f"arXiv論文の取得中にエラー: {e}")
            return None