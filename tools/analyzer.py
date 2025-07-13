"""Gemini APIを使用して論文を解析するクラス"""

import google.generativeai as genai
from paper import Paper
from pdf_processor import PDFProcessor


class GeminiAnalyzer:
    """Gemini APIを使用して論文を解析するクラス"""

    def __init__(self, api_key: str):
        """
        Args:
            api_key: Gemini API キー
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.pdf_processor = PDFProcessor()

    def analyze_paper(self, paper: Paper) -> str:
        """
        論文を解析して要約を生成

        Args:
            paper: 解析する論文

        Returns:
            Markdown形式の要約
        """

        # PDFからテキストを抽出
        pdf_text = self.pdf_processor.process_paper(paper)
        if not pdf_text:
            print(f"PDF処理に失敗しました: {paper.arxiv_id}")
            # フォールバックとしてアブストラクトのみを使用
            pdf_text = paper.abstract

        prompt = f"""
            <paper_summary>
            paper_informationを基に、#0ショートサマリ、#1本研究の概要、#2本研究の新規性や貢献、#3手法、#4評価方法と結果、#5制限事項と課題の各項目ごとに200-400文字程度でまとめてください。
            まとめた各項目の冒頭には## をつけ、項目間には空行を入れてください。

            <paper_information>
            タイトル: {paper.title}
            著者: {paper.authors}
            アブストラクト: {paper.abstract}
            論文全文: {pdf_text}
            </paper_information>

            <#0short_summary>
            本研究の全体の内容について、以下の観点を踏まえて簡素に説明してください:
            - 本研究で解決した問題
            - 本研究を解決した方法
            - 本研究の実験結果
            <note>
            - 論文の内容に忠実に、論文に書かれていない情報や著者の意図を超えた解釈は避けてください。
            - 論文から直接引用する場合は、引用部分を明示してください。
            - 読み手にわかりやすい文章構成を心がけ、段落構成を適切に行い、論理的な流れを意識してください。
            - 専門用語には説明を加えてください。
            - 簡潔かつ明瞭な表現を使用してください。
            </note>
            </#0short_summary>

            <#1summary>
            本研究の概要について、以下の観点を踏まえて詳細に説明してください:
            - 本研究の目的と背景
            - 研究で達成できたこと
            <note>
            - 論文の内容に忠実に、論文に書かれていない情報や著者の意図を超えた解釈は避けてください。
            - 論文から直接引用する場合は、引用部分を明示してください。
            - 読み手にわかりやすい文章構成を心がけ、段落構成を適切に行い、論理的な流れを意識してください。
            - 専門用語には説明を加えてください。
            - 簡潔かつ明瞭な表現を使用してください。
            </note>
            </#1summary>

            <#2novelty_and_contribution>
            本研究の背景について、以下の観点を踏まえて詳細に説明してください:
            - 研究分野の現状と課題
            - 関連する先行研究とその限界や問題点
            - 本研究の位置づけ
            <note>
            - 論文の内容に忠実に、論文に書かれていない情報や著者の意図を超えた解釈は避けてください。
            - 論文から直接引用する場合は、引用部分を明示してください。
            - 読み手にわかりやすい文章構成を心がけ、段落構成を適切に行い、論理的な流れを意識してください。
            - 専門用語には説明を加えてください。
            - 簡潔かつ明瞭な表現を使用してください。
            </note>
            </#2novelty_and_contribution>

            <#3methodology>
            本研究の手法について、以下の観点を踏まえて詳細に説明してください:
            - 使用した技術や手法の概要
            - 研究のアプローチや方法論
            - 特徴的な技術や手法の詳細
            <note>
            - 論文の内容に忠実に、論文に書かれていない情報や著者の意図を超えた解釈は避けてください。
            - 必ず論文から直接引用してください。引用部分を明示してください。
            - 読み手にわかりやすい文章構成を心がけ、段落構成を適切に行い、論理的な流れを意識してください。
            - 専門用語には説明を加えてください。
            - 図表やコードスニペットを活用して、手法の理解を助けてください。
            </note>
            </#3methodology>

            <#4evaluation>
            本研究の評価方法と結果について、以下の観点を踏まえて詳細に説明してください:
            - 実験や評価の方法
            - 得られた結果の概要
            - 結果の解釈や考察
            <note>
            - 論文の内容に忠実に、論文に明示的に書かれている解釈や考察のみを扱ってください。
            - 論文に書かれていない推測や主観的な評価は避けてください。
            - 必ず論文から直接引用してください。引用部分を明示してください。
            - 読み手にわかりやすい文章構成を心がけ、段落構成を適切に行い、論理的な流れを意識してください。
            - 専門用語には説明を加えてください。
            - 著者の主張や論点を明確に伝える文章表現を使用してください。
            </note>
            </#4evaluation>

            <#5limitations_and_challenges>
            本研究の制限事項や課題について、以下の観点を踏まえて詳細に説明してください:
            - 研究の限界や未解決の問題
            - 今後の研究課題や展望
            <note>
            - 論文の内容に忠実に、論文に明示的に書かれている限界や課題のみを扱ってください。
            - 論文に書かれていない推測や主観的な評価は避けてください。
            - 必ず論文から直接引用してください。引用部分を明示してください。
            - 読み手にわかりやすい文章構成を心がけ、段落構成を適切に行い、論理的な流れを意識してください。
            - 専門用語には説明を加えてください。
            - 限界や課題の要点を明確に伝える文章表現を使用してください。
            </note>
            </#5limitations_and_challenges>

            </paper_summary>
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"論文 {paper.arxiv_id} の解析中にエラーが発生しました: {e}")
            return f"# 解析エラー\n\n論文の解析中にエラーが発生しました: {str(e)}"
