# Scaling RL to Long Videos

**arXiv ID**: [2507.07966](http://arxiv.org/abs/2507.07966v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2507.07966v1.pdf)
**著者**: Yukang Chen, Wei Huang, Baifeng Shi, Qinghao Hu, Hanrong Ye, Ligeng Zhu, Zhijian Liu, Pavlo Molchanov, Jan Kautz, Xiaojuan Qi, Sifei Liu, Hongxu Yin, Yao Lu, Song Han
**カテゴリ**: cs.CV, cs.AI, cs.CL
**公開日**: 2025-07-10T17:47:40Z

---

## 要約

## ショートサマリ
本研究は、強化学習を活用し、VLM（Vision-Language Models）の長尺動画における推論能力を拡張するフルスタックフレームワークを提案しています。長尺動画の推論における課題を解決するため、(1) 52Kペアの高品質な動画Q&Aデータセット「LongVideo-Reason」を構築、(2) CoT-SFT（Chain-of-Thought Supervised Fine-Tuning）とRL（Reinforcement Learning）を組み合わせた2段階訓練パイプラインを採用、(3) シーケンス並列処理とvLLMベースのエンジンを統合した効率的な訓練インフラ「MR-SP」を開発しました。実験では、LongVILA-R1-7BがVideoMMEなどの既存ベンチマークで高い性能を示し、独自のLongVideo-Reason-evalベンチマークではGemini-1.5-Proに匹敵する性能を達成しました。また、MR-SPシステムはRL訓練で最大2.1倍の高速化を実現し、長尺動画の訓練を可能にしました。

## 本研究の概要
本研究の目的は、VLM（Vision-Language Models）が長尺動画において複雑な推論を行う能力を、強化学習（RL）を用いて向上させる「フルスタックフレームワーク」を導入することです。長尺動画の理解には、時間的、空間的、目標指向的、物語的な視点からの推論が不可欠である一方、高品質な推論データセットの収集や、長尺動画RL訓練の高い計算コストが大きな課題でした。

本研究では、以下の点を達成しました。(1) 52Kの高品質なQuestion-Reasoning-Answerペアからなる大規模データセット「LongVideo-Reason」を構築しました。(2) VLMsをCoT-SFT（Chain-of-Thought Supervised Fine-Tuning）とRLで拡張する2段階訓練パイプラインを提案しました。(3) 長尺動画RL向けに効率的な訓練インフラ「Multi-modal Reinforcement Sequence Parallelism (MR-SP)」を開発し、メモリ消費を軽減し、訓練を高速化しました。実験では、提案モデルLongVILA-R1-7BがLongVideo-Reason-evalなどのベンチマークで、既存のオープンソースモデルや一部のプロプライエタリモデルを凌駕する強力な性能を達成し、入力フレーム数が増加するにつれて一貫した性能向上を示すことを実証しました。

## 本研究の新規性や貢献
本研究は、VLMが長尺動画の理解において直面する主要な課題に対処しています。現在の研究分野では、長尺動画の理解には時間的、空間的、目標指向的、物語的視点からの高度な推論が求められますが、既存のVLMsではこの能力が限定的です。先行研究（GPT-4o, Gemini-1.5-Pro, Video-R1など）は主に単一画像や短尺動画に焦点を当てており、「long video reasoning still poses great challenges」と筆者は述べています。

また、高品質な長尺動画推論データセットの収集が難しく、コストと時間がかかるという課題があります。さらに、長尺動画における強化学習（RL）訓練は、「computationally expensive and sample-inefficient」であり、「extended video frames, requiring more memory and longer rollout runtime」という問題がありました。シーケンス並列処理は長文脈訓練のメモリ問題に対応しますが、マルチモーダルRLでは、長くて混合されたトークンシーケンスからの大規模なサンプリングが必要となるため、さらなる課題が生じます。本研究は、これらデータと訓練効率の両方のボトルネックに対し、新しい大規模データセット、2段階訓練パイプライン、そして効率的なMR-SP訓練インフラを組み合わせることで、包括的な解決策を提示し、長尺動画推論におけるVLMの能力を大きく前進させるものです。

## 手法
本研究は、長尺動画の推論能力を向上させるため、データセット構築、2段階訓練パイプライン、および効率的な訓練インフラを組み合わせています。

まず、高品質な長尺動画QAデータセット「LongVideo-Reason」を構築しました。約18Kの長尺動画から、「52K high-quality Question-Reasoning-Answer pairs」を自動アノテーションパイプラインで生成しました。このパイプラインは、動画を10秒のクリップに分割し、NVILA-8Bでキャプションを生成後、オープンソースの推論LLMを用いて動画全体にわたる推論を要する質問と回答、そして推論過程を生成します。これらの質問は「Temporal Reasoning, Goal and Purpose Reasoning, Spatial Reasoning, or Plot and Narrative Reasoning」の4種類に分類されます。生成されたデータは、CoT-SFT（18Kサンプル）とRL（33Kサンプルと既存の110K動画データ）にフィルタリングされ、特にRL用データはGRPO（Group Relative Policy Optimization）の特性を考慮し、多様な予測を生む「medium」なサンプルが選ばれます。「GRPO expects different rollouts of each sample to be diverse in order to have meaningful advantages, and the gradient vanishes if all the rollouts predict correct or incorrect answers」。

次に、LongVILA-R1の2段階訓練パイプラインを提案します。
1. **Long CoT-SFT**: 「utilizing 18K data with high-quality CoT for SFT on the MM-SP system」。この段階でモデルに基本的な推論能力と指示追従能力を付与します。
2. **GRPO for Long Video**: CoT-SFTの後、強化学習（RL）を行います。「adhere to the standard GRPO framework to train our model」。ポリシーモデルは旧ポリシーから候補応答グループを生成し、ルールベースの報酬関数（フォーマット/精度）に基づいて報酬が計算されます。「𝒥(𝜃) =E𝑞,{𝑜𝑖}[1𝐺𝐺∑︁𝑖=1(min(𝜋𝜃(𝑜𝑖|𝑞)𝜋𝜃𝑜𝑙𝑑(𝑜𝑖|𝑞)𝐴𝑖,clip(𝜋𝜃(𝑜𝑖|𝑞)𝜋𝜃𝑜𝑙𝑑(𝑜𝑖|𝑞),1−𝜖,1 +𝜖)𝐴𝑖)−𝛽D𝐾𝐿(𝜋𝜃||𝜋𝑟𝑒𝑓))]」。

長尺動画RLの計算負荷に対処するため、「Multi-modal Reinforcement Sequence Parallelism (MR-SP)」フレームワークを開発しました。
1. **Stage 1 - Rollout with Paralleled Encoding**: 「input video frames are first evenly divided across multiple GPUs...Each GPU independently processes a slice of the video...The resulting video embeddings are then aggregated with text embeddings via an all-gather operation」。これにより、エンコーディングの負荷を分散し、メモリオーバーフローを回避します。さらに、「the gathered embeddings are reused during multiple rollouts without recomputation」。
2. **Stage 2 - Prefilling with Sequence Parallelism**: 「globally gathered input embeddings are first padded to a uniform length...and then evenly partitioned across GPUs...This parallelism is applied to both policy and reference model prefilling. Then, each GPU locally computes logits for its token slice, prefilling in parallel」。vLLMエンジンも活用し、高効率なプリフィルを実現します。

## 評価方法と結果
本研究では、LongVILA-R1の性能を評価するために、複数のベンチマークとアブレーションスタディを実施しました。

**実験方法**:
1.  **既存ベンチマークでの性能評価**: 「9 video benchmarks [13,14,18,43,44,45,46,47,48]」を用いて、LongVILA-R1-7BとLongVILA-7Bの性能を比較しました。また、VideoMMEベンチマークでは、様々なビデオ長における既存の先進モデル（Video-LLaVA-7B、Gemini-1.5-Proなど）との比較も行いました。
2.  **LongVideo-Reason-evalベンチマーク**: 新たに構築した「manually curate a balanced set of 1K long-video samples」からなるこのベンチマークは、時間的推論（Temporal Reasoning）、目標・目的推論（Goal and Purpose Reasoning）、空間的推論（Spatial Reasoning）、物語的推論（Plot and Narrative Reasoning）の4つのカテゴリでモデルの推論能力を包括的に評価するために使用されました。
3.  **アブレーションスタディ**:
    *   **入力フレーム数のスケーリング**: LongVILA-1.5BとLongVILA-1.5B-R1モデルにおいて、入力ビデオフレーム数を16から512まで変化させ、LongVideo-Reason-evalにおける推論能力を測定しました。
    *   **訓練パイプラインとデータセットの効果**: LongVILA-1.5Bをベースとして、CoT-SFTとRLの訓練ステージ、および使用するデータセット（本研究のデータセットか既存のオープンソースデータセットか）の組み合わせによる精度への影響を評価しました。
    *   **MR-SPの訓練効率**: A100ノード（8 GPU）上で、MR-SPシステムが長尺動画RL訓練にもたらす高速化効果を測定しました。

**結果の概要**:
*   **既存ベンチマーク**: 「LongVILA-R1-7B consistently outperforms LongVILA-7B across all benchmarks」。VideoMMEでは、「LongVILA-R1-7B achieves the leading scores under different video lengths, obtaining scores of 60.3 and 65.9 in the settings without subtitles and with subtitles, respectively」。
*   **LongVideo-Reason-eval**: 「LongVILA-R1-7B achieves an average accuracy of 67.9% across four reasoning categories, surpassing open-source models including Video-R1-7B [2] and proprietary models such as GPT-4o [19] by a large margin, and matches the performance of Gemini-1.5-Pro [20]」。特に空間的推論では「a score of 70.0」を達成しました。
*   **入力フレーム数のスケーリング**: 「LongVILA-R1-1.5B demonstrates consistent performance improvements throughout the scaling process」で、512フレームで64.3のスコアを達成。LongVILA-1.5Bが256フレームで性能のボトルネックに達し、512フレームで劣化するのとは対照的でした。
*   **訓練パイプラインとデータセットのアブレーション**: 「incorporating RL on top of the warm-up phase (CoT-SFT) yields additional improvements compared to using only SFT」。CoT-SFTなしでRLを行うと精度が低下し、既存データセットのみの使用では性能が劣ることが示されました。
*   **MR-SPの訓練効率**: MR-SPシステムは、「achieves up to a 2.1 ×speedup on 512-frame video RL training on 7B models and enables longer training frames without out-of-memory (OOM)」。

**結果の解釈**:
これらの結果は、LongVILA-R1が長尺動画の推論において非常に強力な能力を持つことを示しています。特に、本研究で構築された高品質なCoTデータセットと、CoT-SFTおよびRLを組み合わせた2段階訓練パイプラインが、モデルの推論能力向上に大きく貢献していることが示唆されます。また、MR-SPの導入により、長尺動画RL訓練における計算効率とメモリの課題が克服され、より長時間の動画処理が可能になったことが、モデル性能のスケールアップに不可欠であることが強調されています。LongVILA-R1は、複雑な長尺動画推論タスクにおいて、既存の先進モデルに匹敵、またはそれを上回る性能を示し、この分野における重要な一歩を記しました。

## 制限事項と課題
本研究にはいくつかの制限事項と今後の研究課題が挙げられています。

まず、データセット構築に関して、「the definition of reasoning still requires further refinement and a more comprehensive conclusion」。推論の定義がまだ完全に洗練されておらず、より包括的な結論が必要であるとしています。

次に、訓練フレームワークの限界についてです。「while our proposed efficient reasoning RL training framework is the first to support video training with hundreds to thousands of frames, real-world scenarios often involve videos with far greater frame counts. Thus, there remains significant potential for improvement in the extraction and learning of ultra-dense visual information」。提案された効率的な強化学習訓練フレームワークは、数百から数千フレームの動画訓練をサポートする初めてのものですが、実際のシナリオではさらに多くのフレーム数を持つ動画が頻繁に存在するため、超高密度視覚情報（ultra-dense visual information）の抽出と学習には、依然として改善の大きな可能性があると述べています。

将来的な展望として、本研究の進展は「embodied AI, robotics, autonomous systems, and AR/VR applications」など、多様なドメインに革新的な可能性をもたらすと述べています。長尺動画データの処理と推論能力をVLMに持たせることで、「AI systems capable of understanding event sequences, tracking object persistence and transformations, and inferring causal and physical relationships over extended frames」の基盤を築きます。また、「AI tutors to analyze and summarize extended instructional videos, or assist healthcare professionals in reviewing lengthy procedural recordings. Furthermore, such systems could enhance sports analytics, and other areas requiring nuanced temporal reasoning」といった応用が期待されます。

しかし、「unlocking the full promise of this technology requires a steadfast commitment to ethical principles, privacy protection, and the broader goal of benefiting humanity」。この技術の潜在能力を最大限に引き出すためには、倫理原則、プライバシー保護、そして人類全体への貢献という広範な目標への揺るぎないコミットメントが必要であると強調しています。

---

*このファイルは自動生成されました。生成日時: 2025年07月13日 12:46:16*
