# Scaling RL to Long Videos

**arXiv ID**: [2507.07966](http://arxiv.org/abs/2507.07966v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2507.07966v1.pdf)
**著者**: Yukang Chen, Wei Huang, Baifeng Shi, Qinghao Hu, Hanrong Ye, Ligeng Zhu, Zhijian Liu, Pavlo Molchanov, Jan Kautz, Xiaojuan Qi, Sifei Liu, Hongxu Yin, Yao Lu, Song Han
**カテゴリ**: cs.CV, cs.AI, cs.CL
**公開日**: 2025-07-10T17:47:40Z

---

## 要約

## ショートサマリ
本研究は、強化学習（RL）を活用して、VLM（Vision-Language Models）の長尺動画における推論能力をスケールアップさせるフルスタックフレームワークを提案します。長尺動画推論の課題に対処するため、(1) 52Kの高品質な推論アノテーションを含む大規模データセット「LongVideo-Reason」、(2) CoT-SFT（Chain-of-Thought Supervised Fine-Tuning）とRLを組み合わせた2段階訓練パイプライン、(3) 効率的な長尺動画RL訓練インフラ「MR-SP（Multi-modal Reinforcement Sequence Parallelism）」を統合しました。実験では、LongVILA-R1-7BがVideoMMEなどのベンチマークで優れた性能を発揮し、Gemini-1.5-Proに匹敵しました。特にMR-SPシステムはRL訓練で最大2.1倍の高速化を達成し、GPUのOOM（Out-Of-Memory）問題を回避しました。

## 本研究の概要
本研究は、長尺動画におけるVLM（Vision-Language Models）の推論能力向上を目的としています。長尺動画の理解には、時間的、空間的、目標指向的、物語的な多角的な推論が不可欠ですが、その実現には「高品質な長尺動画推論データセットの収集」と「計算コストの高い強化学習（RL）訓練」という特有の課題がありました。

本研究では、これらの課題を解決する包括的なフレームワーク「LongVILA-R1」を導入しました。これにより、(1) 52Kの高品質な「Question-Reasoning-Answer」ペアを含む大規模データセット「LongVideo-Reason」を構築し、(2) CoT-SFT（Chain-of-Thought Supervised Fine-Tuning）と強化学習を組み合わせた2段階の訓練パイプラインを開発しました。さらに、(3) 大量の視覚埋め込みや長コンテキストLLMプリフィルといった、長尺動画RLの計算負荷を軽減する効率的な訓練インフラ「MR-SP（Multi-modal Reinforcement Sequence Parallelism）」を提案しました。LongVILA-R1-7Bは、既存の長尺動画QAベンチマークで優れた性能を示し、入力フレーム数が増加しても一貫して性能が向上することを確認しました。

## 本研究の新規性や貢献
長尺動画の理解は、時間的・空間的・目標指向的・物語的観点からの複雑な推論を必要とします。しかし、既存のVLM（Vision-Language Models）は主に単一画像や短尺動画に焦点を当てており、長尺動画における推論能力には大きな課題がありました。特に、高品質な長尺動画推論データセットの構築は、複雑な時間的ダイナミクスや物語要素のアノテーションが労力とコストを要するため困難でした。また、強化学習（RL）はモデルの推論目標を調整する有効な戦略ですが、長尺動画に適用すると、膨大なフレーム数によりメモリと実行時間が長くなり、計算コストがさらに増大するという問題がありました。

先行研究では、Sequence Parallelism (SP) などが長コンテキスト訓練のメモリ効率を改善しましたが、マルチモーダルRLはさらに複雑なサンプリングと高い計算コストを伴い、既存のRLフレームワークでは長尺動画の訓練に対応できませんでした。

本研究は、これらの課題に対処するため、長尺動画推論のためのフルスタックフレームワーク「LongVILA-R1」を提案しました。主要な貢献は、(1) 高品質なCoTアノテーションを含む大規模データセット「LongVideo-Reason」の構築、(2) CoT-SFTとRLを組み合わせた2段階訓練パイプラインの導入、(3) 長尺動画RL訓練に特化した、効率的かつスケーラブルな訓練インフラ「MR-SP」の開発です。これにより、長尺動画の推論におけるVLMの能力を大幅に向上させ、既存のボトルネックを克服しました。

## 手法
本研究は、強化学習を用いてVLM（Vision-Language Models）の長尺動画における推論能力を向上させる包括的なフレームワーク「LongVILA-R1」を提案しています。このフレームワークは、主に「大規模データセットの構築」、「2段階訓練パイプライン」、そして「効率的な訓練インフラ」という3つのコンポーネントから構成されます。

まず、高品質なデータセット「LongVideo-Reason」を構築しました。これは、18Kの長尺動画からNVILA-8Bモデルで生成されたクリップキャプションを基に、リーディングオープンソース推論LLMを用いて52Kの「Question-Reasoning-Answer」ペアを生成したものです。これらのペアは時間的、目標/目的、空間的、物語的推論の4つのカテゴリに分類され、視覚的詳細に焦点を当てるように「checking the video」や「analyzing the scene」といったフレーズでプロンプトが設計されました。

次に、2段階の訓練パイプラインを採用しました。(1) **ステージ1: Long CoT-SFT (Chain-of-Thought Supervised Fine-Tuning)**では、フィルタリングされた18Kの高品質CoTデータセットを使用し、MM-SP（Multi-modal Sequence Parallelism）システムを用いてモデルの基本的な推論能力と指示追従スキルをウォームアップします。(2) **ステージ2: GRPO (Group Relative Policy Optimization) for Long Video**では、CoT-SFTでウォームアップされたモデルをさらにスケールアップさせるため、33Kの挑戦的なQ&Aサンプルと追加の110Kのオープンソース動画データを使用します。このRL段階では、「policy model generates a group of candidate responses {𝑜1, 𝑜2, ..., 𝑜𝐺} from the old policy 𝜋𝜃𝑜𝑙𝑑, accompanied by their corresponding rewards {𝑟1, 𝑟2, ..., 𝑟𝐺}」を生成し、ポリシーを最適化します。

最後に、長尺動画RLの計算負荷に対処するため、効率的な訓練インフラ「MR-SP（Multi-modal Reinforcement Sequence Parallelism）」を開発しました。MR-SPは以下の2段階で構成されます。
- **ステージ1 - Rollout with Paralleled Encoding**: 「The input video frames are first evenly divided across multiple GPUs (e.g., GPU 1 to GPU 3), each equipped with its own vision tower. Each GPU independently processes a slice of the video, encoding only a subset of the frames. The resulting video embeddings are then aggregated with text embeddings via an all-gather operation」。これにより、エンコーディングのワークロードが分散され、より長い動画の処理が可能になります。集約された埋め込みは、複数のロールアウトで再計算なしに再利用されます。
- **ステージ2 - Prefilling with Sequence Parallelism**: 「we parallelize the inference stage across devices using sequence parallelism. As illustrated in Figure 7, we globally gathered input embeddings are first padded to a uniform length (Padding Sequence) and then evenly partitioned across GPUs (Sharding to Local GPU).」これにより、各GPUが入力シーケンスの一部のみを処理し、ポリシーモデルと参照モデルの両方のプリフィルが並列化され、vLLMベースのエンジンとキャッシュされた動画埋め込みを活用して訓練を加速します。

## 評価方法と結果
本研究では、LongVILA-R1-7Bの性能を多角的に評価しました。まず、ActNet-QA、EgoSchema、EventBench、LVideoBench、PercepTest、MVBench、NExT-QA、VNBench、VideoMMEの9つの既存ビデオベンチマークで性能比較を行いました。「LongVILA-R1-7Bは、既存の全ベンチマークにおいてLongVILA-7Bを一貫して上回っており、推論タスクの複雑さに応じて性能差がある」ことが示されました。特にVideoMMEベンチマークでは、字幕付き設定で68.4%のスコアを達成し、Short、Medium、Longの各動画長で既存モデルと比較してリードするスコアを記録しました。

次に、本研究で構築した新しいベンチマーク「LongVideo-Reason-eval」において、LongVILA-R1-7BをGPT-4o、Gemini-1.5-Pro、Video-R1-7Bと比較しました。このベンチマークは、時間的、目標/目的、空間的、物語的推論の4つのカテゴリで構成されています。LongVILA-R1-7Bは平均67.9%の精度を達成し、Video-R1-7BやGPT-4oを大幅に上回り、Gemini-1.5-Proに匹敵する性能を示しました。「特に、空間推論カテゴリではLongVILA-R1-7Bが70.0%のスコアを達成している」ことが特筆されます。

さらに、アブレーションスタディを実施しました。入力フレーム数のスケーリングに関する実験では、LongVILA-R1-1.5Bが入力フレーム数（16から512まで）の増加に伴い、一貫して推論性能が向上し、512フレームで64.3%を達成しました。訓練パイプラインとデータセットのアブレーションでは、CoT-SFTとRLを組み合わせた訓練が最も高い精度（61.9%）を示し、CoT-SFTがRLの前段階として重要であることが確認されました。

最後に、MR-SPシステムの訓練効率を評価しました。シングルA100ノード（8基のA100 GPU）での実験の結果、「MR-SPシステムは、512フレームの動画RL訓練において最大2.1倍の高速化を達成し、OOMなしで1024フレームまで効率的にスケールできる」ことが実証されました。これらの結果は、LongVILA-R1が長尺動画におけるVLMの推論能力と訓練効率の両方を大幅に向上させることを明確に示しています。

## 制限事項と課題
本研究は長尺動画の推論能力を向上させる画期的なフレームワークを提案しましたが、いくつかの制限事項と今後の課題を認識しています。まず、高品質な長尺動画推論データセットの構築に最善を尽くしたものの、「推論の定義はさらなる洗練とより包括的な結論を必要としている」と述べています。これは、推論の複雑な性質を完全に捉えることの難しさを示唆しています。

次に、提案された効率的な強化学習（RL）訓練フレームワークは、「数百から数千フレームの動画訓練をサポートする初めてのものである」としながらも、「実世界のシナリオでははるかに多くのフレーム数の動画が含まれることが多い」ことを指摘しています。このことから、超高密度な視覚情報から意味のある情報を抽出し、学習する能力にはまだ大きな改善の可能性があることが今後の課題として挙げられます。

将来的には、LongVILA-R1のような技術が、Embodied AI、ロボティクス、自律システム、AR/VRアプリケーションなど、幅広い分野で「洗練された時間的および複合的な理解を実行することを可能にする」と期待されています。しかし、この技術の可能性を最大限に引き出すためには、「倫理原則、プライバシー保護、および人類に利益をもたらすという広範な目標への確固たるコミットメントが必要」であると強調しており、技術の進歩と並行して社会的な側面にも配慮していく必要があります。

---

*このファイルは自動生成されました。生成日時: 2025年07月13日 04:22:46*
