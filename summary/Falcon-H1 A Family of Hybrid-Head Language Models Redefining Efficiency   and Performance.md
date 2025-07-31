# Falcon-H1: A Family of Hybrid-Head Language Models Redefining Efficiency   and Performance

**arXiv ID**: [2507.22448](http://arxiv.org/abs/2507.22448v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2507.22448v1.pdf)
**著者**: Jingwei Zuo, Maksim Velikanov, Ilyas Chahed, Younes Belkada, Dhia Eddine Rhayem, Guillaume Kunsch, Hakim Hacid, Hamza Yous, Brahim Farhat, Ibrahim Khadraoui, Mugariya Farooq, Giulia Campesan, Ruxandra Cojocaru, Yasser Djilali, Shi Hu, Iheb Chaabane, Puneesh Khanna, Mohamed El Amine Seddik, Ngoc Dung Huynh, Phuc Le Khac, Leen AlQadi, Billel Mokeddem, Mohamed Chami, Abdalgader Abubaker, Mikhail Lubinets, Kacper Piskorski, Slim Frikha
**カテゴリ**: cs.CL
**公開日**: 2025-07-30T07:55:33Z

---

## 要約

## #0ショートサマリ

本研究は、大規模言語モデル（LLMs）における性能と効率の両立という課題を解決するため、Falcon-H1シリーズを提案します。本モデルは、TransformerベースのアテンションとState Space Models（SSMs）を並列に組み合わせたハイブリッドアーキテクチャを採用し、モデル設計、データ戦略、訓練ダイナミクスを包括的に見直しました。実験結果として、Falcon-H1は卓越したパラメータ効率と訓練効率で最先端の性能を示しました。特に、フラッグシップのFalcon-H1-34Bは、半分のパラメータと少ないデータで70Bスケールのモデル（Qwen3-32B, Qwen2.5-72B, Llama3.3-70Bなど）に匹敵するか、それを上回る性能を発揮しました。小規模モデルも同様の傾向を示し、推論、数学、多言語、指示追従、科学知識などの広範なタスクで優位性を確立しました。

## #1本研究の概要

本研究の目的は、Transformerモデルの二次的な計算複雑性や、高性能と高効率の両立といったLLM開発における主要な課題に対処することです。State Space Models（SSMs）が長文コンテキスト処理と計算効率に優れるという知見に基づき、本研究はTransformerの強力なアテンションメカニズムとSSMの長所を組み合わせた新しいハイブリッドアーキテクチャを導入しました。

これにより、Falcon-H1という新しいLLMシリーズが開発され、0.5Bから34Bまでの様々なパラメータスケールで、ベースモデルと指示チューニング済みモデルがリリースされました。本研究で達成できたことは、先行のFalconモデル（TransformerまたはMamba単体）とは異なり、並列ハイブリッド設計を採用し、モデル設計、データ戦略、訓練ダイナミクスのあらゆる側面を体系的に再検討した結果、Falcon-H1モデルが最先端（SOTA）の性能と卓越したパラメータ効率および訓練効率を達成したことです。特に、主力モデルのFalcon-H1-34Bは、少ないパラメータとデータで、70Bスケールの競合モデルと同等かそれを上回る性能を発揮しました。

## #2本研究の新規性や貢献

研究分野の現状として、Transformerアーキテクチャは入力シーケンス長に対して計算コストが二次的に増加するという課題を抱えています。このため、Multi-head Latent Attention（MLA）のような効率的な代替案や、MambaなどのTransformerを完全に超える新しいアーキテクチャが模索されています。また、アテンションとSSMの補完的な強みを組み合わせるハイブリッドモデル（Jamba、Sambaなど）も登場しています。

しかし、先行研究におけるハイブリッドモデルの多くはSSMとアテンションを逐次的に統合しており、アテンションとSSMのチャネル比率を独立して調整する柔軟性に欠けていました。また、Mambaアーキテクチャは比較的新しく、そのハイパーパラメータの詳細な探索が不足していました。

本研究は、これらの課題に対し、Transformer型アテンションとMambaベースSSMを「並列に統合する革新的なハイブリッドアーキテクチャ」を採用することで位置づけられます。その新規性は、「アテンションとMambaヘッドの量を独立して調整できる」柔軟性を提供し、最適なアテンションとSSMの比率を可能にした点にあります。この設計により、Falcon-H1は高速な推論、低いメモリ使用量、そして幅広いベンチマークでの最先端性能を実現し、既存のLLMシリーズとは一線を画しています。

## #3手法

本研究では、高性能と高効率を両立するLLMを開発するため、いくつかの特徴的な手法とアプローチを採用しています。

まず、基盤となるアーキテクチャは、TransformerベースのアテンションとState Space Models（SSMs）を並列に組み合わせたハイブリッド設計です。「Attention and SSM run in parallel within each block; their outputs are concatenated before the block’s output projection.」という独自の並列ハイブリッドデザインにより、柔軟なチャネル割り当てが可能になりました。先行研究では探求されていなかった「This flexibility has not been explored in previous hybrid designs.」と論文は述べており、実験により「semi-parallel SA_M configuration provides the best results」を導き出しました。

次に、SSM固有のハイパーパラメータ（状態次元 `dstate`、ヘッド次元 `dhead`、深層畳み込みカーネルサイズなど）と、アテンション/SSM/MLPチャネルの割り当てを小規模モデルで詳細にアブレーション研究することで、最適な設定を特定しました。特に、RoPE（Rotary Positional Embedding）のベース周波数には「unconventionally high value b= 10^11 of the RoPE base frequency.」を設定し、長文コンテキストへの対応力を高めました。さらに、幅と深さのトレードオフを検討し、「greater depth yielded consistently higher overall quality」であることを見出し、より深いモデルの優位性を示しました。

訓練ダイナミクスの安定化のため、訓練初期の損失スパイクの主な原因が「width-related dynamics inside the SSM—specifically the larger number of heads—as a primary driver of the observed instability」であることを診断し、「A softer alternative is to multiply the dt activation by a constant 0< α < 1.」という減衰を適用して安定化させました。また、学習率（LR）と重み減衰（WD）の影響を「effective learning rate (ELR) ηeff=√η/λ and effective weight decay (EWD) λeff=√λ/η」として定義し直すことで、パラメータノルムとノイズレベルがそれぞれELRとEWDによって制御されることを経験的に示し、ハイパーパラメータ調整を効率化しました。

データ戦略では、ウェブデータ、多言語データ、コードデータ、数学データ、自社生成の合成データを組み合わせた包括的なコーパスを構築しました。特に、高品質なデータを反復利用する「マルチエポック訓練」や、訓練初期からあらゆる複雑さのデータを導入する「アンチカリキュラム」アプローチを採用しました。トークナイザもモデルサイズに応じて語彙サイズをスケーリングし、句読点と数字の分割、LaTeXトークンの組み込みを行いました。

分散訓練では、自社開発の「Mambatron」フレームワークを使用し、標準の3次元並列に加えて、長文コンテキスト向けのコンテキスト並列（CP）と、アテンションとSSMの計算を並行して実行する「Mixer Parallelism (MP)」を導入しました。「we partitioned the Tensor Parallel (TP) world into two distinct groups: one dedicated to Mamba operations, the other to attention operations.」というMPは、「interleaved Mixer Parallelism achieves a substantial 1.43x speedup over the baseline」を達成しました。

## #4評価方法と結果

本研究の評価は、既存のオープンソースフレームワークである「lm-evaluation-harness、evalchemy、evalplus、helmet」を基盤とし、公平性を期すために全てのモデルを同一のDocker環境で評価しました。Qwen3シリーズについては「"thinking mode"を無効化」し、evalchemyの数学ベンチマークでは「生成ターン数16に標準化し、同一システムプロンプトを適用、最終結果はMath-Verifyで後処理」されました。モデル効率はFalcon-H1-34BとQwen2.5-32BをvLLMで比較しました。

得られた結果は、Falcon-H1シリーズが「state-of-the-art performance with remarkable training efficiency」を達成したことを示しています。訓練データ量が「modest 2.5T to 18T tokens」であるにもかかわらず、競合モデルを凌駕する性能を一貫して示しました。例えば、Falcon-H1-0.5Bはサブ1Bモデルの新たなベンチマークとなり、1.5B-Deepモデルは7B-10Bモデルに匹敵する性能を発揮しました。フラッグシップのFalcon-H1-34Bは、70Bスケールの競合モデルと比較して、BBH、MATH-lvl5、GPQA、すべてのコード生成タスク、MGSMでSOTA性能を達成し、そのパラメータ効率が際立ちました。

長文コンテキスト能力においては、Falcon-H1-34B-InstructがHELMETスイートで評価され、特に「our model uniquely achieves the top score on RAG at 131k tokens (62.21), surpassing all competitors, including those more than twice its size」というRAGタスクで優れた性能を示しました。モデル効率の比較では、長文シーケンスにおいてFalcon-H1-34BがQwen2.5-32Bと比較して「up to a 4x improvement in input throughput and an 8x speedup in output throughput」を達成しました。

結果の解釈として、これらの成果は「革新的なハイブリッドMamba-Transformerアーキテクチャ」と「カスタマイズされたトレーニング戦略」の成功に起因すると考えられます。特に、1.5B-Deepモデルの成功は、深層アーキテクチャが推論集約型タスクで強力な汎化能力と多価的なスキルをもたらすことを示唆しています。また、長文コンテキストでの推論効率の大幅な向上は、Mambaベースのアーキテクチャの強みを明確に示しています。「The initial advantage of the Transformer-based model at short contexts is likely attributable to the highly mature optimizations of attention mechanisms within modern inference frameworks compared to current State-Space Model (SSM) implementations. As theoretically, Mamba-based or hybrid architectures are more efficient, we believe this gap highlights a promising direction for future work.」と論文は考察しており、SSM実装のさらなる最適化の余地を示唆しています。

## #5制限事項と課題

本研究の制限事項と課題として、まず「モデルの性能が、特に小規模なモデルでは、訓練の終了時においても飽和していなかった」ことが挙げられます。これは、現在の訓練予算ではモデルの潜在能力を最大限に引き出せていない可能性を示唆しています。

次に、長文コンテキストの評価において、「純粋なリコールや長文質問応答タスクでは、Qwen3-32BやLlama-3.3-70Bのような競合モデルに、特に極端なコンテキスト長で劣る」という性能ギャップが確認されました。論文は、「この性能差はアーキテクチャの制限ではなく、訓練データ構成に起因する」と推測しており、「よりキュレーションされた長文コンテキストデータ」によって改善できる余地があると述べています。

また、モデル効率の比較において、短コンテキストでTransformerベースのモデルが優位性を示すのは、「現代の推論フレームワークにおけるアテンションメカニズムの成熟した最適化」によるものであり、現在のState-Space Model（SSM）実装と比較して改善の余地があるとしています。論文は、「このギャップは将来の研究の有望な方向性」であり、「コミュニティにSSM実装の最適化への貢献を呼びかけている」と明記しています。

さらに、本研究で提案された効果的な学習率（ELR）と効果的な重み減衰（EWD）に関する結論は、「限定された実験に基づく大まかな近似」であり、「これらの問題の正確な調査は将来の研究にとって刺激的な方向性となる」と述べられています。モデルの深さによるµP乗数のスケーリングは、「単純化と時間の制約により適用しなかった」ため、これも今後の課題です。

今後の研究課題としては、「データ強化」を最優先し、ベースモデルと指示チューニング済みモデルの両方を、より広範で多様な高品質データセットをキュレーションすることで、繰り返し改良していく予定です。また、「アーキテクチャとアルゴリズムの革新」を継続し、特に「効果的な知識圧縮と、256kを超えるコンテキストへのスケーリング」に焦点を当てます。最終的に、「モデルのコア推論能力を深化させるための新しい技術を探求し、戦略的にモデルをスケールアップし続ける」ことで、「SOTAであるだけでなく、根本的に効率的でアクセスしやすいモデルの開発」を目指すとしています。

---

*このファイルは自動生成されました。生成日時: 2025年07月31日 08:35:36*
