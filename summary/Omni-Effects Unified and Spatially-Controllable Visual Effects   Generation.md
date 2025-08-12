# Omni-Effects: Unified and Spatially-Controllable Visual Effects   Generation

**arXiv ID**: [2508.07981](http://arxiv.org/abs/2508.07981v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2508.07981v1.pdf)
**著者**: Fangyuan Mao, Aiming Hao, Jintao Chen, Dongxia Liu, Xiaokun Feng, Jiashu Zhu, Meiqi Wu, Chubin Chen, Jiahong Wu, Xiangxiang Chu
**カテゴリ**: cs.CV, cs.AI
**公開日**: 2025-08-11T13:41:24Z

---

## 要約

## ショートサマリ
本研究は、現代映画制作に不可欠な視覚効果（VFX）生成において、既存モデルが単一効果に限定され、複数の効果を特定の場所に同時に生成する空間制御可能な複合効果に対応できないという根本的な課題を解決します。提案手法「Omni-Effects」は、初の統合フレームワークであり、プロンプトガイドによる効果生成と空間制御可能な複合効果生成を可能にします。その核となるのは、「LoRA-based Mixture of Experts (LoRA-MoE)」による多様な効果の統合とタスク間干渉の軽減、そして空間マスク情報をテキストトークンに組み込む「Spatial-Aware Prompt (SAP)」による正確な空間制御です。さらに、SAP内の「Independent-Information Flow (IIF)」により、個々の制御信号の分離を実現します。広範な実験により、Omni-Effectsが正確な空間制御と多様な効果生成を両立し、ユーザーが効果の種類と場所を柔軟に指定できることを実証しました。

## 本研究の概要
本研究は、現代の映画制作に不可欠な視覚効果（VFX）の制作における課題解決を目的としています。既存のビデオ生成モデルはVFX制作にコスト効率の良い解決策を提供するものの、効果ごとのLoRA (Low-Rank Adaptation) トレーニングに制約され、生成が単一の効果に限定されるという根本的な限界がありました。この制約により、複数の効果を特定の場所に同時に生成する「空間的に制御可能な複合効果（spatially controllable composite effects）」を必要とするアプリケーションが妨げられていました。また、多様な効果を統一フレームワークに統合する際には、効果の変動による干渉や、複数VFX（マルチVFX）の合同トレーニング中の空間制御不能性といった大きな課題がありました。

これらの課題を克服するため、本研究では「Omni-Effects」という初の統合フレームワークを提案しました。このフレームワークは、プロンプトガイドによる効果生成と空間的に制御可能な複合効果生成を可能にします。主な達成点は、第一に、一連のエキスパートLoRAを使用し、多様な効果を統一モデル内で統合しつつ、タスク間の干渉を効果的に軽減する「LoRA-based Mixture of Experts (LoRA-MoE)」の導入です。第二に、空間マスク情報をテキストトークンに組み込むことで正確な空間制御を可能にする「Spatial-Aware Prompt (SAP)」を考案しました。さらに、SAPに統合された「Independent-Information Flow (IIF)」モジュールにより、個々の効果に対応する制御信号を分離し、意図しないブレンドを防ぎました。これにより、ユーザーは希望する効果の種類と場所の両方を指定できるようになりました。研究を促進するために、包括的なVFXデータセット「Omni-VFX」と、専用のVFX評価フレームワークも構築しました。

## 本研究の新規性や貢献
本研究の背景には、現代のVFX制作におけるビデオ生成モデルの利用が進む中で、従来のパイプラインが抱える複雑さとリソース集約型であるという課題があります。特に、複数の異なる空間位置で同時調整を必要とする複合効果は、従来のVFXパイプラインでは複雑かつリソースを消費するとされています。既存のビデオ生成手法は、VFXデータの希少性と、効果間で動的特性が大きく異なるという課題に直面しています。このため、「現在の手法は単一効果の生成に焦点を当てており、個々の効果に特化したLoRA（Low-Rank Adaptation）を採用しています。」("current methods focus on single-effect generation, employing dedicated Low-Rank Adaptation (LoRA) tailored to individual effects.")。

しかし、このパラダイムはマルチVFXシーンにおいて2つの重大な限界を抱えています。第一に、「複数LoRAの同時活性化は空間的なオクルージョンアーティファクトを誘発し、タスク干渉を通じて忠実度を低下させるクロスエフェクト混同を引き起こします。」("joint multi-LoRA activation induces spatial occlusion artifacts ... and shared-subspace hybrid training triggers fidelity-degrading cross-effect confusion via task interference.")。第二に、「テキストとピクセルの空間的ギャップがVFX配置の正確な空間キューエンコーディングを妨げます。」("the text-pixel space gap prevents precise spatial cue encoding for VFX placement.")。例えば、ControlNet (Zhang et al., 2023)は空間制御に利用されますが、モデルパラメータの重複による「大きなパラメータオーバーヘッド」("Significant parameter overhead")と、マルチVFX生成時の「深刻なクロスコンディション干渉」("Severe cross-condition interference")という問題がありました。

本研究は、これらの限界を克服するため、マルチVFX生成を多条件ビデオ生成問題としてモデル化する「初の統合フレームワーク」("a first unified framework")である「Omni-Effects」を提案することで位置づけられます。これにより、高忠実度のマルチVFX合成をピクセルレベルの空間制御で実現し、従来の技術が抱えていた相互干渉や空間制御の課題を解決します。本研究の主要な貢献は、(1) 「LoRA-MoEモジュール」と「IIF拡張SAPメカニズム」を統合した統一VFXフレームワークの提案、(2) 「自動生成パイプラインを備えた最も包括的なVFXデータセットOmni-VFX」と評価フレームワークの開発、そして (3) 広範な実験による「正確な空間制御と多様なVFX生成」の達成です。

## 手法
本研究で提案する「Omni-Effects」は、ビデオ拡散モデルの「CogVideoX (Yang et al., 2024) アーキテクチャ」を基盤とし、マルチVFX生成を多条件ビデオ生成問題として扱います。核となるのは、「LoRA-based Mixture of Experts (LoRA-MoE)」と「Spatial-Aware Prompt (SAP)」の2つのコンポーネントです。

まず、「LoRA-MoE」は、従来のFFN（Feed-Forward Network）線形層を置き換えるMoEプラグインとして機能します。これは、「各LoRAが異なるVFX多様体に特化するエキスパートアンサンブル」を採用しています。具体的には、入力トークン$x \in R^d$に対し、ゲーティングネットワーク$G: R^d \to R^n$が各エキスパート$E_i$の重み$G(x)_i$を計算し、最終的な出力は「$y = \text{Base}(x) + \sum_{i=1}^n G(x)_i \odot E_i(x)$」として結合されます。これにより、多様な効果を統一モデル内で統合し、タスク間の干渉を効果的に軽減します。推論時には、効果の抑制を防ぐためにすべてのエキスパートが活性化されます。また、訓練時のワークロード不均衡を軽減するために、「バランスルーティング補助損失$L_{aux}$」が適用されます。

次に、「Spatial-Aware Prompt (SAP)」は、VFXのテキスト記述子と空間トリガーを融合させ、正確な空間制御を可能にします。従来のテキストプロンプトによる位置記述では、「注意はプロンプトのセマンティクスに関わらず常に同一の領域を活性化」("attention consistently activates identical regions regardless of prompt semantics")するため、正確な空間制御が困難でした。SAPは、テキスト条件トークン$ \{ \tau^{(i)}_e(e_i) \}_{i=1}^N $と空間条件トークン$ \{ \tau^{(i)}_s(s_i) \}_{i=1}^N $をノイズのある潜在$x_t$と共に連結し、クエリQ、キーK、バリューVを形成します。さらに、「Independent-Information Flow (IIF)」モジュールがSAPに統合されています。IIFは、特別に設計された注意マスク$M \in \{0, -\infty\}^{l \times l}$（$l$は全シーケンス長）を利用し、「条件間の、そしてノイズから条件への相互作用をブロック」("blocks condition-to-condition and noise-to-condition interactions")することで、クロスコンディション情報漏洩を防ぎ、意図しない効果の混同やミスマッチを排除します。注意の最終出力は「$y = \text{Softmax}(\frac{QK^T}{\sqrt{d_k}} + M)V$」として表現されます。

訓練データが単一VFXのみでマルチVFXデータを含まないという課題に対しては、トリレベルの解決策を採用しています。データレベルでは、「ランダムなクロッピングと2つのビデオでのスプライシング、およびランダムな時間的フリーズ」("through random cropping and splicing with two videos, and random temporal freezing")により、対応するマスクを持つ「擬似マルチVFXビデオ」を生成します。スケジューラレベルでは、「非均一サンプリング」("Non-Uniform Sampling")により、空間制御学習に重要な早期のデノイジングステップ（例えば900-1000ステップ）に重点を置きます。訓練戦略レベルでは、「反復的な単一からマルチVFX（$N=2$）へのファインチューニング」("iterative single to multi-VFX ($N=2$) fine-tuning")によって安定した収束と性能向上を実現します。

## 評価方法と結果
本研究では、Omni-Effectsの有効性を評価するため、包括的な実験を行い、既存のベースラインモデルと比較しました。

**実験セットアップと評価指標:**
評価には、まず「包括的なVFXデータセットOmni-VFXを構築し、専用のVFX評価フレームワークを導入」("construct a comprehensive VFX dataset Omni-VFX ... and introduce a dedicated VFX evaluation framework")しました。Omni-VFXは、画像編集とFLF2V (First-Last Frame-to-Video) 合成を組み合わせたデータ収集パイプラインで構築され、55種類のVFXカテゴリを網羅しています。
単一VFXの評価には、全体的な忠実度を測る「FVD (Fréchet Video Distance)」と、動きのダイナミクスを測る「Dynamic Degree」を使用しました。制御可能なVFXの評価では、新たに3つの指標を導入しました。1. 「Regional Dynamic Degree (RDD)」は、ターゲット領域内の動きの強さを定量化します。2. 「Effect Occurrence Rate (EOR)」は、意図した効果の出現頻度を測定し、生成の信頼性を示します。これは、ビデオとプロンプトをGemini 2.5 (Comanici et al., 2025)に入力し、VFXの存在を判定することで算出されます。3. 「Effect Controllability Rate (ECR)」は、EORに基づいてVFXが指定領域に限定されているかを確認し、空間精度を評価します。ベースラインモデルとして、CogVideoX、LTX-Video、Wan2.1、そしてControlNetを統合したCogVideoX (CogV+CN) が比較対象となりました。

**得られた結果と解釈:**
1.  **統一VFX生成**: 「LoRA-MoEは、OpenVFXデータセットにおいて、異なるタイプのVFXで最高の性能を達成し、訓練可能なパラメータ数を大幅に削減しました。」("LoRA-MoE achieves the best performance across different types of VFX, while significantly reducing the number of trainable parameters.")。これは、「設計されたVFXタスク部分空間分割戦略の有効性」("effectiveness of the designed VFX task-subspace partitioning strategy")を実証しています。

2.  **制御可能VFX生成**:
    *   **単一VFX制御**: 表2に示すように、ベースライン手法はターゲットVFXの合成と正確な空間制御において根本的な限界を示しました。特に「CogV+CNはVFXを合成できるものの、制御可能性は限定的」("While CogV+CN can synthesize VFX, it exhibits limited controllability")でした。対照的に、「Omni-Effectsは0.97 EORと0.88 ECRで最高の性能を達成し、生成品質と空間制御精度の両方ですべてのベースラインを大幅に上回りました。」("Omni-Effects achieves the best performance with 0.97 EOR and 0.88 ECR, significantly outperforming all baselines in both generation quality and spatial control precision.")。これにより、「我々の提案するSAPが、実質的な追加訓練パラメータを導入することなく、VFX記述子を空間トリガーと効果的に統合する」("our proposed SAP effectively integrates VFX descriptors with spatial triggers without introducing substantial additional training parameters")ことが検証されました。

    *   **マルチVFX制御**: 表3と図6に示すように、ベースラインモデルがマルチVFX生成や空間制御に失敗する中で、Omni-Effectsは「同時VFXに対して正確な空間制御を達成」("achieves precise spatial control over simultaneous VFX")しました。例えば、左の椅子を溶かし、右の椅子を浮上させる指示に対し、CogVideoXは両方のオブジェクトに溶融を誤って適用し、CogV+CNは溶融は正しくレンダリングするものの浮上を生成できませんでしたが、「Omni-Effectsは空間条件を通じて両方のVFXを同時に実行しました。」("Omni-Effects simultaneously executes both VFX through spatial condition.")。この結果は、「我々の提案するIIFがクロスコンディション干渉を軽減する有効性」("our proposed IIF’s efficacy in mitigating cross-condition interference")を検証するものです。

3.  **汎化性能**: 「N=2の効果のみで訓練されたにもかかわらず、本モデルは共有の空間条件LoRAを使用することで推論時に多様なマスク条件に汎化し、より多くの同時制御VFX（N>2）の生成に拡張可能である」("Despite being trained with only N=2 effects, our model generalizes to diverse mask conditions during inference using the shared Spatial-Condition LoRA, thereby extending to the generation of more concurrent control VFX (N > 2)")ことを示しました。

## 制限事項と課題
本研究は、多条件VFX生成の分野において大きな進歩をもたらしましたが、論文の「Conclusion」や「Introduction」セクションから、いくつかの限界や今後の課題が示唆されています。

まず、**データセットの制約**が挙げられます。論文では、「我々の訓練データセットは単一VFXのみで、マルチVFXデータを含まない」("our training dataset contains only single-VFX without multi-VFX data")と明記されています。このため、制御可能なマルチVFX生成を実現するために、「ランダムなクロッピングと2つのビデオでのスプライシング、およびランダムな時間的フリーズ」("through random cropping and splicing with two videos, and random temporal freezing")によって擬似マルチVFXビデオを生成するというデータ拡張手法が必要でした。これは、実際のマルチVFXデータが不足している現状を反映しており、将来的にはより大規模かつ多様な実際のマルチVFXデータセットの構築が望ましいと考えられます。

次に、**モデルの複雑性と最適化の課題**です。LoRA-MoEに関するアブレーション研究（Table 4）では、「エキスパートのスケーリングは生成品質を向上させるが、パラメータコストも増加する」("scaling experts improves generation quality at increased parameter cost")ことが示されています。これは、性能向上と計算リソースの効率性との間にトレードオフが存在することを示しており、最適なエキスパート数やモデル構成の探求が今後の課題となる可能性があります。

最後に、論文は「マルチVFX生成は、実用的な価値が大きく、永続的な技術的課題を伴う領域である」("Multi-VFX generation represents a domain of substantial practical value coupled with persistent technical challenges")と結論付けており、本研究がこの「複雑な問題に明示的に対処する最初の包括的なフレームワーク」("pioneers the first comprehensive framework explicitly addressing this complex problem")であると述べています。これは、本研究がこの分野の基礎を築いたものであり、まだ多くの未解決の課題が残されていることを示唆しています。今後の研究課題としては、より複雑で動的なVFXの合成、より高度な空間的・時間的制御、そして現実世界の多様なシーンへの適用範囲の拡大などが考えられます。また、「我々の手法は、制御可能なマルチVFX合成能力を実質的に進展させ、映画制作、ゲーム開発、広告クリエイティブにおける新たなアプリケーションを解き放つ」("Our methodology substantively advances controllable multi-VFX synthesis capabilities while unlocking novel applications across film production, game development, and advertising creatives")と述べていることから、これらの応用分野でのさらなる発展が期待されます。

---

*このファイルは自動生成されました。生成日時: 2025年08月12日 08:32:52*
