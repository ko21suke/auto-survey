"""論文を取得するための基底クラス"""

import feedparser
import re
from typing import List, Optional
from abc import ABC, abstractmethod
from paper import Paper


class Fetcher(ABC):
    """論文を取得するための基底クラス"""

    def __init__(self):
        """初期化処理"""
        pass

    @abstractmethod
    def fetch_papers(self, **kwargs) -> List[Paper]:
        """
        論文を取得する抽象メソッド

        サブクラスで実装する必要があります

        Returns:
            List[Paper]: 取得した論文のリスト
        """
        pass

    def extract_arxiv_id(self, text: str) -> Optional[str]:
        """
        テキストからarXiv IDを抽出する共通メソッド

        Args:
            text: 検索対象のテキスト

        Returns:
            str: arXiv ID（見つからない場合はNone）
        """
        if not text:
            return None

        # パターン1: arxiv.org/abs/XXXX.XXXXX
        match = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', text)
        if match:
            return match.group(1)

        # パターン2: arXiv:XXXX.XXXXX
        match = re.search(r'arXiv:(\d{4}\.\d{4,5})', text)
        if match:
            return match.group(1)

        # パターン3: /papers/YYYY.YYYYY (Hugging Face URL pattern)
        match = re.search(r'/papers/(\d{4}\.\d{4,5})', text)
        if match:
            return match.group(1)

        # パターン4: 単独のID (XXXX.XXXXX)
        match = re.search(r'\b(\d{4}\.\d{4,5})\b', text)
        if match:
            return match.group(1)

        return None

    def remove_html_tags(self, text: str) -> str:
        """
        HTMLタグを除去する共通メソッド

        Args:
            text: HTMLタグを含むテキスト

        Returns:
            str: HTMLタグを除去したテキスト
        """
        return re.sub(r'<[^>]+>', '', text)

    def parse_feed(self, feed_url: str) -> feedparser.FeedParserDict:
        """
        RSSフィードをパースする共通メソッド

        Args:
            feed_url: RSSフィードのURL

        Returns:
            feedparser.FeedParserDict: パースされたフィード
        """
        return feedparser.parse(feed_url)

    def create_paper(self, **kwargs) -> Paper:
        """
        Paperオブジェクトを作成する共通メソッド

        Args:
            **kwargs: Paper作成に必要な引数

        Returns:
            Paper: 作成されたPaperオブジェクト
        """
        return Paper(**kwargs)