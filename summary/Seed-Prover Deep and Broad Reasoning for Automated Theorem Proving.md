# Seed-Prover: Deep and Broad Reasoning for Automated Theorem Proving

**arXiv ID**: [2507.23726](http://arxiv.org/abs/2507.23726v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2507.23726v1.pdf)
**著者**: Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing Jin, Chenggang Li, Kaijing Ma, Cheng Ren, Jiawei Shen, Wenlei Shi, Tong Sun, He Sun, Jiahui Wang, Siran Wang, Zhihong Wang, Chenrui Wei, Shufa Wei, Yonghui Wu, Yuchen Wu, Yihang Xia, Huajian Xin, Fan Yang, Huaiyuan Ying, Hongyi Yuan, Zheng Yuan, Tianyang Zhan, Chi Zhang, Yue Zhang, Ge Zhang, Tianyun Zhao, Jianqiu Zhao, Yichi Zhou, Thomas Hanwen Zhu
**カテゴリ**: cs.AI, cs.CL
**公開日**: 2025-07-31T17:00:30Z

---

## 要約

## ショートサマリ
本研究は、大規模言語モデル（LLM）が自然言語では定理証明に明確な教師信号を欠くため困難という課題に対し、Leanのような形式言語の自動検証能力を活用する「Seed-Prover」を提案します。これは補題（lemma）スタイルによる全証明推論モデルで、Leanのフィードバックや自己要約に基づき反復的に証明を洗練します。また、深い推論と幅広い推論を実現する3段階の推論戦略を導入。幾何学問題には専用の「Seed-Geometry」エンジンも開発しました。実験では、形式化された過去のIMO問題の78.1%を証明、MiniF2Fでほぼ100%を達成し、既存手法を大幅に上回りました。IMO 2025では6問中5問を完全に証明し、自動数学推論の大きな進歩を示しました。

## 本研究の概要
本研究は、大規模言語モデル（LLM）が数学的推論能力を持つ一方で、自然言語での定理証明においては明確な教師信号の不足から強化学習が困難であるという問題に取り組んでいます。Leanのような形式言語は、証明の自動検証を可能にし、効果的な訓練のための明確な信号を提供します。この背景から、本研究は、Leanのフィードバック、証明済み補題、自己要約に基づいて証明を繰り返し洗練できる、補題スタイルの全証明推論モデル「Seed-Prover」を提案しました。また、IMOレベルの難解な問題に対応するため、深い推論と幅広い推論を可能にする三つの推論戦略を設計しています。さらに、Leanの幾何学サポートの不足を補うために、既存の形式幾何学エンジンを凌駕する幾何学推論エンジン「Seed-Geometry」も導入しました。これにより、形式化された過去のIMO問題の78.1%を証明し、MiniF2Fをほぼ飽和させ、PutnamBenchで50%以上の正解率を達成。IMO 2025では6問中5問を完全に証明するなど、自動数学的推論における顕著な進歩を達成しました。

## 本研究の新規性や貢献
大規模言語モデル（LLM）は数学的推論能力を示すものの、自然言語での証明は検証が難しく、強化学習の適用に課題がありました。Leanのような形式言語は自動検証を可能にするため、この分野ではLLMを用いた証明器の開発が進んでいます。先行研究では、Leanコードを逐次生成するステップレベル証明器と、一度に全証明を生成する全証明生成モデルがありましたが、ステップレベルは粒度が細かすぎ、全証明モデルはLeanコンパイラとの相互作用が不足するという限界がありました。また、Leanには幾何学問題への十分なサポートがないという課題も存在しました。

本研究は、これらの課題に対し、「Seed-Prover」によって「補題スタイル」の全証明モデルを提案し、Leanコンパイラフィードバック、証明済み補題、自己要約に基づく「反復的証明洗練」を可能にしました。これにより、従来の全証明モデルの課題を克服しています。さらに、Light、Medium、Heavyの三段階の「テスト時推論戦略」を導入することで、深い推論と幅広い探索を両立させ、IMOレベルの困難な問題に対応する能力を大幅に向上させました。また、専用の幾何学推論エンジン「Seed-Geometry」を導入することで、Leanの幾何学サポートの不足を補い、幾何学問題解決において既存のAlphaGeometry 2などを凌駕する新たなSOTA（State-of-the-Art）を確立しました。これらの貢献により、本研究は形式検証と長い思考連鎖推論を組み合わせた自動数学的推論の分野で大きな進歩を達成しています。

## 手法
本研究では、「Seed-Prover」と「Seed-Geometry」という二つのシステムを導入しています。

**Seed-Prover**は、Lean 4に特化した大規模言語モデルで、補題（lemma）スタイルの証明を中核に据えています。その特徴として、「Lemma-Style Proving」があります。これは「Seed-Prover tries to generate useful intermediate lemmas before proving the main statement. These lemmas serve as shared knowledge across different inference paths.」と述べられており、主要な定理の前に有用な中間補題を生成し、これを共有知識として利用します。次に、「Iterative Proof Refinement」として、「Seed-Prover iteratively refines its proof based on Lean compiler feedback, previous proved lemmas, and self-summarization.」とあり、Leanコンパイラのフィードバック、以前証明された補題、自己要約に基づいて証明を反復的に洗練します。また、「Test-Time Scaling」として、Light、Medium、Heavyの三つの推論戦略を設計。Light設定は反復的な証明洗練、Medium設定は困難な補題に対する内側洗練、Heavy設定は数千もの推測（conjecture）を生成し、その証明・反証を通じて重要な補題を蓄積し、最終証明に活用します。訓練はVAPOに基づく多段階・多タスク強化学習で行われ、多様な情報（自然言語ヒント、失敗した試み、Leanフィードバックなど）をプロンプトに組み込むことで適応性を高めています。

**Seed-Geometry**は、幾何学推論エンジンであり、TongGeometryを大幅に再設計したものです。その手法は、定規とコンパスの原理に基づきながら、冗長な作図ステップをグループ化し、ドメイン固有言語を拡張しています。推論エンジンはC++で再記述され、「roughly 100-fold speed increase compared to the Python implementation in TongGeometry.」とあり、約100倍の高速化を実現しました。これにより、深層探索が効率化されます。また、高性能なSeedファミリーLLMを用いて、補助的な幾何学的要素の構築を提案し、ビームサーチと分散処理を組み合わせた広範な探索を行います。

## 評価方法と結果
本研究では、Seed-ProverとSeed-Geometryの性能を多角的に評価しました。

**Seed-Prover**は、IMO 2025、過去のIMO問題、MiniF2F、PutnamBench、CombiBench、MiniCTX-v2といった幅広い数学ドメインのベンチマークでテストされました。IMO問題やMiniF2Fでは、未解決問題に対しLight、Medium、Heavyの順に推論設定を適用。PutnamBenchとCombiBenchではLightとMedium設定を使用しました。

結果として、Seed-Proverは以下の性能を示しました。
*   IMO 2025では「5 out of 6 problems」を完全に証明しました（Table 3）。
*   過去のIMO問題155問中121問を証明し、「overall success rate of 78.1%」を達成しました（Table 3）。
*   MiniF2F-validで100.0%、MiniF2F-testで99.6%の飽和に近い証明率を達成しました（Table 3）。
*   PutnamBenchでは657問中331問を証明し、先行研究を大幅に上回りました（Table 3）。
*   CombiBenchでは100問中30問を証明し、前例を上回りました（Table 3）。
*   MiniCTX-v2では「81.8%」を達成し、実世界の自動定理証明における高い汎化能力を示しました（Table 3）。

**Seed-Geometry**は、IMO geometry problems from 2000 to 2024 (IMO-AG-50) とIMO shortlist geometry problems from 2000 to 2022のベンチマークでAlphaGeometry 2と比較されました。

結果として、Seed-Geometryは以下の性能を示しました。
*   IMO-AG-50では「43 problem solves compared to AlphaGeometry 2」の42問を上回り、新記録を樹立しました（Table 1）。
*   IMO Shortlistでは39問中22問を解決し、AlphaGeometry 2の19問を上回りました（Table 2）。
*   IMO 2025 P2をわずか2秒で解決しました。

これらの結果は、「Seed-Prover proves 78.1% of formalized past IMO problems, saturates MiniF2F, and achieves over 50% on PutnamBench, outperforming the previous state-of-the-art by a large margin.」および「Seed-Geometry, which outperforms previous formal geometry engines.」というアブストラクトの記述を裏付け、両システムがそれぞれの分野で最先端の性能を達成していることを示しています。

## 制限事項と課題
本研究は自動数学的推論において大きな進歩を遂げましたが、いくつかの制限事項や今後の課題も存在します。

まず、**Seed-Prover**に関して、IMO 2025では「fully prove 5 out of 6 problems」とあり、全ての問題を証明できたわけではありません。また、組合せ論に特化した「CombiBench」の評価では、「Nonetheless, relative to other benchmarks, our model still struggles with proving combinatorics problems.」と明記されており、他のベンチマークと比較して組合せ論の問題解決に苦戦していることが示されています。これは、これらの問題が「often involve newly-defined concepts」であることに起因すると考えられます。

次に、**Seed-Geometry**に関して、IMO-AG-50でSeed-Geometryが解決できなかった問題については、「not proof-based problems but rather computation-based problems, which AlphaGeometry 2 could potentially address using its algebraic engine.」と説明されており、証明ベースではない計算ベースの問題への対応が課題として挙げられます。

今後の研究課題として、論文の結論部では「Our future work will focus on combining formal systems with large language models to tackle open conjectures.」と述べられており、未解決の数学的な推測（open conjectures）に取り組むことが挙げられています。これは、現在のシステムの能力をさらに拡張し、新たな数学的発見に貢献することを目指すものです。組合せ論の問題解決能力の向上や、計算ベースの幾何学問題への対応も、具体的な改善点として考えられます。

---

*このファイルは自動生成されました。生成日時: 2025年08月01日 08:33:27*
