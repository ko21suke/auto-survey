"""arXivのRSSフィードから論文情報を取得するクラス"""

from typing import List
from fetchers.base import Fetcher
from paper import Paper


class ArxivRSSFetcher(Fetcher):
    """arXivのRSSフィードから論文情報を取得するクラス"""

    def __init__(self):
        super().__init__()
        self.base_url = "https://rss.arxiv.org/rss/"
        self.cs_categories = [
            "cs",  # Computer Science (all)
            "cs.AI",  # Artificial Intelligence
            "cs.CL",  # Computation and Language
            "cs.CC",  # Computational Complexity
            "cs.CE",  # Computational Engineering
            "cs.CG",  # Computational Geometry
            "cs.CR",  # Cryptography and Security
            "cs.CV",  # Computer Vision and Pattern Recognition
            "cs.CY",  # Computers and Society
            "cs.DB",  # Databases
            "cs.DC",  # Distributed, Parallel, and Cluster Computing
            "cs.DL",  # Digital Libraries
            "cs.DM",  # Discrete Mathematics
            "cs.DS",  # Data Structures and Algorithms
            "cs.ET",  # Emerging Technologies
            "cs.FL",  # Formal Languages and Automata Theory
            "cs.GL",  # General Literature
            "cs.GR",  # Graphics
            "cs.GT",  # Computer Science and Game Theory
            "cs.HC",  # Human-Computer Interaction
            "cs.IR",  # Information Retrieval
            "cs.IT",  # Information Theory
            "cs.LG",  # Machine Learning
            "cs.LO",  # Logic in Computer Science
            "cs.MA",  # Multiagent Systems
            "cs.MM",  # Multimedia
            "cs.MS",  # Mathematical Software
            "cs.NA",  # Numerical Analysis
            "cs.NE",  # Neural and Evolutionary Computing
            "cs.NI",  # Networking and Internet Architecture
            "cs.OH",  # Other Computer Science
            "cs.OS",  # Operating Systems
            "cs.PF",  # Performance
            "cs.PL",  # Programming Languages
            "cs.RO",  # Robotics
            "cs.SC",  # Symbolic Computation
            "cs.SD",  # Sound
            "cs.SE",  # Software Engineering
            "cs.SI",  # Social and Information Networks
            "cs.SY",  # Systems and Control
        ]

    def fetch_papers(self, category: str = "cs", max_results: int = 10) -> List[Paper]:
        """
        指定したカテゴリから論文を取得

        Args:
            category: arXivのカテゴリ (デフォルト: "cs" - 全ての情報科学)
            max_results: 取得する論文の最大数

        Returns:
            Paper オブジェクトのリスト
        """
        if category not in self.cs_categories:
            raise ValueError(f"カテゴリ {category} は情報科学のカテゴリではありません")

        feed_url = f"{self.base_url}{category}"
        print(f"フィードURL: {feed_url} から論文を取得中...")

        try:
            feed = self.parse_feed(feed_url)
            papers = []

            for entry in feed.entries[:max_results]:
                # arXiv IDを抽出（共通メソッドを使用）
                arxiv_id = self.extract_arxiv_id(entry.link) if hasattr(entry, 'link') else ""

                # PDFリンクを生成
                pdf_link = f"https://arxiv.org/pdf/{arxiv_id}.pdf" if arxiv_id else ""

                # 論文情報を作成（共通メソッドを使用）
                paper = self.create_paper(
                    arxiv_id=arxiv_id,
                    title=entry.title,
                    authors=entry.author if hasattr(entry, 'author') else "著者不明",
                    abstract=self._extract_abstract(entry.description),
                    category=entry.tags[0].term if hasattr(entry, 'tags') and entry.tags else category,
                    published=entry.published if hasattr(entry, 'published') else "",
                    link=entry.link,
                    pdf_link=pdf_link
                )
                papers.append(paper)

            print(f"{len(papers)}件の論文を取得しました")
            return papers

        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return []

    def _extract_abstract(self, description: str) -> str:
        """
        RSSフィードのdescriptionから要約を抽出

        Args:
            description: RSSフィードのdescriptionタグの内容

        Returns:
            抽出された要約
        """
        # HTMLタグを除去（共通メソッドを使用）
        abstract = self.remove_html_tags(description)

        # arXiv IDとAnnounce Typeの部分を除去
        import re
        abstract = re.sub(r'arXiv:\d+\.\d+v?\d*\s*Announce Type:.*?\n', '', abstract)

        # Abstract:という文字列以降を取得
        if 'Abstract:' in abstract:
            abstract = abstract.split('Abstract:', 1)[1]

        return abstract.strip()