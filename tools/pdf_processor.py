"""PDFファイルのダウンロードとテキスト変換を行うモジュール"""

import os
import requests
import PyPDF2
import shutil
from typing import Optional
from paper import Paper


class PDFProcessor:
    """PDFファイルのダウンロードとテキスト変換を行うクラス"""

    def __init__(self, pdf_dir: str = "../temp_pdfs"):
        """
        Args:
            pdf_dir: PDFファイルを保存するディレクトリ
        """
        self.pdf_dir = pdf_dir
        os.makedirs(pdf_dir, exist_ok=True)

    def download_pdf(self, paper: Paper) -> Optional[str]:
        """
        論文のPDFをダウンロード

        Args:
            paper: Paper インスタンス

        Returns:
            ダウンロードしたPDFファイルのパス、失敗時はNone
        """
        pdf_filename = f"{paper.arxiv_id.replace('/', '_')}.pdf"
        pdf_path = os.path.join(self.pdf_dir, pdf_filename)

        # 既にダウンロード済みの場合はスキップ
        if os.path.exists(pdf_path):
            print(f"PDF already exists: {pdf_path}")
            return pdf_path

        try:
            # PDFをダウンロード
            response = requests.get(paper.pdf_link, timeout=30)
            response.raise_for_status()

            # ファイルに保存
            with open(pdf_path, 'wb') as f:
                f.write(response.content)

            print(f"PDF downloaded: {pdf_path}")
            return pdf_path

        except requests.RequestException as e:
            print(f"Failed to download PDF: {e}")
            return None

    def pdf_to_text(self, pdf_path: str) -> Optional[str]:
        """
        PDFファイルをテキストに変換

        Args:
            pdf_path: PDFファイルのパス

        Returns:
            抽出したテキスト、失敗時はNone
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                # 全ページからテキストを抽出
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()

                return text

        except Exception as e:
            print(f"Failed to extract text from PDF: {e}")
            return None

    def process_paper(self, paper: Paper) -> Optional[str]:
        """
        論文のPDFをダウンロードしてテキストに変換

        Args:
            paper: Paper インスタンス

        Returns:
            抽出したテキスト、失敗時はNone
        """
        # PDFをダウンロード
        pdf_path = self.download_pdf(paper)
        if not pdf_path:
            return None

        # テキストに変換
        text = self.pdf_to_text(pdf_path)
        return text

    def cleanup_temp_files(self):
        """
        一時PDFファイルを全て削除
        """
        if os.path.exists(self.pdf_dir):
            try:
                shutil.rmtree(self.pdf_dir)
                print(f"Temporary PDF directory '{self.pdf_dir}' has been removed")
            except Exception as e:
                print(f"Failed to remove temporary PDF directory: {e}")