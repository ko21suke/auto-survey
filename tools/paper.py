"""論文情報を格納するデータクラス"""

from dataclasses import dataclass


@dataclass
class Paper:
    """論文情報を格納するデータクラス"""
    arxiv_id: str
    title: str
    authors: str
    abstract: str
    categories: str
    published: str
    link: str
    pdf_link: str