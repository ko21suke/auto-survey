# ReasonRank: Empowering Passage Ranking with Strong Reasoning Ability

**arXiv ID**: [2508.07050](http://arxiv.org/abs/2508.07050v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2508.07050v1.pdf)
**著者**: Wenhan Liu, Xinyu Ma, Weiwei Sun, Yutao Zhu, Yuchen Li, Dawei Yin, Zhicheng Dou
**カテゴリ**: cs.IR, cs.AI, cs.CL, cs.LG
**公開日**: 2025-08-09T17:26:18Z

---

## 要約

## #0ショートサマリ
本研究は、推論を必要とする複雑な検索シナリオにおいて、既存の再ランク付けモデルが訓練データの不足により性能が低いという課題を解決します。この課題に対し、まずDeepSeek-R1を用いた自動推論集約型訓練データ合成フレームワークと、品質を確保する自己整合性データフィルタリング機構を提案。次に、強力な推論能力を持つリストワイズ再ランク付けモデル「ReasonRank」を強化するため、冷スタートSFT（教師ありファインチューニング）と、リストワイズランキングの性質に合わせた多視点ランキング報酬を設計した強化学習（RL）からなる2段階後学習アプローチを導入しました。実験により、ReasonRankは既存のベースラインを大幅に上回り、BRIGHTリーダーボードでSOTA（最先端）性能40.6を達成し、ポイントワイズ再ランク付けモデルRank1よりも低いレイテンシ（低遅延）を実現しました。

## #1本研究の概要
本研究は、大規模言語モデル（LLM）ベースのリストワイズランキング（リスト全体を考慮してランキングを行う手法）が多くのタスクで優れた性能を示す一方で、推論を必要とする複雑な検索シナリオでは、既存の再ランク付けモデルの性能が低いという問題意識から出発しました。これは、推論集約型の訓練データが不足していることに主な原因があります。

本研究の目的は、このデータ不足と推論能力の欠如を克服し、複雑な検索クエリに対応できる強力な推論能力を備えた高性能なリストワイズ再ランク付けモデルを開発することです。

研究を通じて達成できたことは以下の通りです。まず、多様なドメイン（複雑なQA、コーディング、数学、ウェブ検索）から高品質な推論集約型訓練データを自動合成するフレームワークを確立しました。次に、この合成データと、ReasonRankの推論・ランキング能力を高める2段階の学習アプローチ（冷スタートSFTと強化学習）を提案しました。これにより開発されたReasonRankは、推論集約型IR（情報検索）ベンチマークであるBRIGHTおよびR2MEDにおいて、既存のベースラインを大幅に上回るSOTA性能を達成しました。さらに、ポイントワイズ（各文書とクエリの関連性を個別に評価する手法）の再ランク付けモデルよりも効率的であることも実証しました。

## #2本研究の新規性や貢献
情報検索分野において、LLMベースのリストワイズランキングは目覚ましい進歩を遂げていますが、推論集約型検索シナリオにおけるランキング能力は未発達という現状があります。これは、既存の再ランク付けモデルが、単純な語彙的・意味的マッチングに重点を置いたMSMARCOのような従来のウェブ検索データで主に訓練されており、StackExchangeのような複雑な推論を伴う現実世界の検索クエリに対応できないためです。推論集約型訓練データの不足が大きな課題であり、人間によるアノテーションは高コストで非現実的でした。

関連する先行研究として、Rank1やRank-KといったモデルがDeepSeek-R1の推論チェーンを蒸留し、再ランク付けモデルに推論能力を注入しようと試みています。また、一部のRLベースの再ランク付けモデルはNDCG（情報検索の評価指標の一つ）を報酬として利用していますが、スライディングウィンドウベースのリストワイズランキングにおける複数ターンの性質を考慮していないため、最適とは言えません。

本研究は、これらの限界を克服するために独自のアプローチを提案します。主な貢献は以下の通りです。
「`To address the scarcity of reasoning-intensive ranking data, we design an automated data synthesis framework that generates 13K high-quality and diverse reasoning-intensive training data for the reasoning-intensive ranking task.`」（推論集約型ランキングデータの不足に対処するため、推論集約型ランキングタスク向けに13Kの高品質で多様な推論集約型訓練データを生成する自動データ合成フレームワークを設計しました。）
「`we propose a two-stage training framework, which includes a cold-start SFT strategy for reasoning pattern learning and a multi-view ranking reward-based RL approach for further ranking ability enhancement.`」（推論パターン学習のための冷スタートSFT戦略と、ランキング能力のさらなる向上のための多視点ランキング報酬ベースのRLアプローチを含む2段階の訓練フレームワークを提案します。）
これらの貢献により、ReasonRankは推論集約型IRベンチマークでSOTA性能と効率性の両方を示しました。

## #3手法
本研究では、強力な推論能力を持つリストワイズ再ランク付けモデルReasonRankを開発するため、主に「推論集約型ランキングデータ合成」と「2段階訓練フレームワーク」という二つの主要な手法を採用しています。

**1. 推論集約型ランキングデータ合成:**
推論集約型訓練データの不足を解消するため、自動データ合成フレームワークを提案します。
- **データソース:** 複雑なQA（StackExchange）、コーディング（Leetcode）、数学（MATH）、およびウェブ検索（MSMARCO）という多様なドメインからクエリとパッセージを収集します。
- **ラベル生成:** 強力な推論モデルDeepSeek-R1（R1）を用いて、各クエリに対するポジティブパッセージとハードネガティブパッセージをマイニングし、高品質な訓練ラベル（推論チェーンとゴールドランキングリスト）を生成します。R1がクエリをよりよく理解し、より良いランキングラベルを生成できるよう、ゴールドアンサーをR1に供給します。
- **自己整合性データフィルタリング:** 「`we believe that the labels with higher self-consistency from R1 should have higher quality. Thus, we calculate the ranking metric NDCG@10 for the gold ranking lists in listwise labels using the pointwise labels and filter out training samples with NDCG@10 below a threshold α.`」（R1からの自己整合性が高いラベルは高品質であると信じ、リストワイズラベルのゴールドランキングリストのNDCG@10をポイントワイズラベルを用いて計算し、NDCG@10が閾値α（0.4）未満の訓練サンプルをフィルタリングします。）これにより、合成データの品質を確保します。

**2. 2段階訓練フレームワーク:**
合成された高品質なリストワイズ訓練データに基づき、以下の2段階アプローチでReasonRankを訓練します。
- **冷スタートSFT（Supervised Fine-Tuning）:**
  「`We first introduce a cold-start Supervised Fine-Tuning (SFT) strategy to help the backbone LLM learn the listwise reasoning pattern as well as the gold ranking list.`」（まず、バックボーンLLMがリストワイズ推論パターンとゴールドランキングリストを学習するのを助けるため、冷スタートSFT戦略を導入します。）推論チェーンと再ランク付けリストを含むリストワイズラベルを用いて、標準の言語モデリング損失を最小化することでモデルを最適化します。
- **多視点ランキングに基づくRL（Reinforcement Learning）:**
  「`Then, we use Reinforcement Learning (RL) to help LLM explore better reasoning patterns and enhance the LLM’s ranking ability.`」（次に、LLMがより良い推論パターンを探求し、LLMのランキング能力を強化するために、強化学習（RL）を使用します。）RLアルゴリズムGRPOを採用し、SFTで訓練されたモデルのランキング性能をさらに向上させます。
  - **多視点ランキング報酬 `Rm`:** スライディングウィンドウベースのリストワイズランキングの性質を考慮し、従来のランキングメトリック（NDCG@10）に加えて、Recall@10（上位10件に存在する関連パッセージの割合）とRBO（Rank-Biased Overlap：ランキングの類似度を測る指標）を組み合わせた報酬を設計します。「`Thus, besides NDCG@10, we propose to incorporate metric Recall@10 as a part of our ranking reward. Furthermore, compared to using pointwise labels for NDCG@10 computation, we contend that the gold list in our listwise labels contains more granular ranking signals. Consequently, we use the rank-biased overlap (RBO) metric (Webber, Moffat, and Zobel 2010), which measures the ranking similarity as another supplementary ranking reward.`」
  - 最終的な報酬Rは、出力フォーマットの正しさも考慮して計算されます。「`To ensure proper output structure, we implement format rewards considering two kinds of formats: (1) output format which ensures the presence of both <think> and <answer> tags, and (2) answer format that validates the content within <answer> tags adheres to the specified ranking list format ( e.g., [4] > [2] > . . . ).`」

バックボーンLLMにはQwen2.5-7B-InstructとQwen2.5-32B-Instructを使用し、LoRA（Low-Rank Adaptation：大規模モデルの効率的なファインチューニング手法）アダプターを用いて効率的な訓練を行います。

## #4評価方法と結果
本研究では、ReasonRankの有効性と効率性を評価するため、複数の情報検索ベンチマークと詳細なアブレーションスタディを実施しました。

**実験方法:**
- **評価データセット:** 推論集約型IRベンチマークとしてBRIGHTとR2MEDを使用。さらに、伝統的なIRベンチマークであるBEIRの7つのデータセットで汎化能力を評価しました。
- **初期リトリーバー:** BRIGHTではReasonIR (8B)、R2MEDではE5-Mistral-7B-Instructを初期検索器として使用し、BEIRではBM25を使用しました。いずれの場合も、上位100件の検索結果を再ランク付けしました。
- **評価指標:** NDCG@10（Normalized Discounted Cumulative Gain at 10: 検索結果の上位10件の関連度と順位を考慮した指標）を使用しました。
- **比較対象:** 非推論型再ランク付けモデル（RankT5、RankZephyr）と推論型再ランク付けモデル（Rank1、Rank-R1、Rank-K）を比較しました。
- **効率性分析:** ReasonRank (7B) とポイントワイズ（各文書とクエリの関連性を個別に評価する手法）のRank1 (7B) のクエリあたりのレイテンシ（遅延）を比較しました。
- **アブレーションスタディ:** 訓練データ（MSMARCOのみ使用、自己整合性フィルタリングなし）と訓練アプローチ（SFTなし、RLなし、多視点報酬なし、非推論SFT）の各コンポーネントの寄与を検証しました。

**得られた結果と考察:**
- **主要な性能:** 「`Our ReasonRank (7B and 32B) demonstrate superior performance compared with all baselines on Avg. of two benchmarks.`」（ReasonRank (7Bおよび32B) は、両ベンチマークの平均で全てのベースラインと比較して優れた性能を示しました。）特にReasonRank (32B) はBRIGHTリーダーボードでSOTA（最先端）性能40.6を達成し、既存のどのベースラインよりも大幅に優れていました。これは、提案されたデータ合成と2段階訓練フレームワークの有効性を示唆しています。
- **既存ベースラインの課題:** 既存のベースラインは推論集約型再ランク付けにおいて苦戦しており、初期検索結果からの改善が難しい場合が多く、伝統的な訓練データや手法では効果的な推論集約型再ランク付けモデルの生成が困難であることが示されました。
- **モデルサイズと性能:** 再ランク付けモデルの性能はモデルサイズに比例して向上することが確認され、大規模モデルがより強力な推論・ランキング能力を持つことが示されました。
- **効率性:** 「`our listwise ReasonRank is 2-2.7× faster than pointwise Rank1`」（リストワイズのReasonRankはポイントワイズのRank1よりも2〜2.7倍高速でした。）これは、Rank1が各パッセージに対して推論チェーンを生成するのに対し、ReasonRankは一度に複数のパッセージを処理し、1つの推論チェーンしか生成しないため、出力トークン数が大幅に減少することに起因します。
- **アブレーションスタディ:**
    - 多様な推論集約型ドメインからの訓練データ構築が不可欠であり、MSMARCOサブセットのみでは性能が大幅に低下することが確認されました。
    - 自己整合性データフィルタリングの有効性も実証されました。
    - 2段階訓練フレームワークの各ステージ（特に冷スタートSFT）が、推論パターン学習とランキング能力強化に不可欠であることが示されました。
    - 多視点ランキング報酬 (`Rm`) が性能向上に寄与することが証明されました。
    - 推論がReasonRankの有効性を大幅に強化することも確認されました。
- **さらなる性能向上:** より高品質な検索結果（RaDeR + BM25）や、より小さいスライディングウィンドウサイズ（窓サイズ10、ストライド5）を使用することで、ランキング性能をさらに向上できることが示されました。

## #5制限事項と課題
本研究のReasonRankは優れた性能を達成したものの、いくつかの制限事項と今後の研究課題を抱えています。

- **推論モードと非推論モードの切り替え:**
  「`ReasonRank does not include non-reasoning type data during training, which results in its inability to seamlessly switch between reasoning and non-reasoning modes when faced with search scenarios of varying difficulty.`」（ReasonRankは訓練中に非推論型のデータを含んでいないため、難易度が異なる検索シナリオに直面した場合に、推論モードと非推論モードをシームレスに切り替えることができません。）このため、将来の研究では、ReasonRankの柔軟性を高めるために、非推論タイプのデータを訓練セットに導入する予定です。

- **バックボーンLLMの多様性:**
  「`we only use Qwen2.5-series LLMs as the backbones for ReasonRank and did not use other models (such as Llama 3.1 (Dubey et al. 2024) and reasoning-based models Qwen3 (Yang et al. 2025a)).`」（本研究では、ReasonRankのバックボーンとしてQwen2.5-series LLMのみを使用しており、他のモデル（Llama 3.1や推論ベースモデルQwen3など）は使用していません。）今後は、他のモデルを基盤としてReasonRankの有効性を検証し、その汎用性を確認する予定です。

- **スライディングウィンドウ戦略への依存:**
  「`ReasonRank still relies on the sliding window strategy for passage reranking. Existing study (Liu et al. 2024b) have demonstrated that LLMs have strong full-list ranking capabilities (i.e., directly ranking 100+ passages in one forward pass), which exhibit both superior efficiency and effectiveness compared to sliding window approaches.`」（ReasonRankはパッセージの再ランク付けに依然としてスライディングウィンドウ戦略に依存しています。既存の研究（Liu et al. 2024b）では、LLMがフルリストランキング（すなわち、1回のフォワードパスで100以上のパッセージを直接ランキング）において強力な能力を持ち、スライディングウィンドウアプローチと比較して優れた効率性と有効性の両方を示すことが実証されています。）将来の研究では、フレームワークのスケーラビリティと性能をさらに向上させるため、フルリストランキングに基づいた推論集約型リストワイズ再ランク付けの探求を計画しています。

---

*このファイルは自動生成されました。生成日時: 2025年08月12日 08:32:10*
