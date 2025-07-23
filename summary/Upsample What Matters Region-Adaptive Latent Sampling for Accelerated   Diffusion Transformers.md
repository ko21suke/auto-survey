# Upsample What Matters: Region-Adaptive Latent Sampling for Accelerated   Diffusion Transformers

**arXiv ID**: [2507.08422](http://arxiv.org/abs/2507.08422v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2507.08422v1.pdf)
**著者**: Wongi Jeong, Kyungryeol Lee, Hoigi Seo, Se Young Chun
**カテゴリ**: cs.CV, eess.IV
**公開日**: 2025-07-11T09:07:43Z

---

## 要約

## ショートサマリ
本研究は、Diffusion Transformers (DiTs) の高い計算コストを解決するため、学習不要な空間次元高速化フレームワーク「Region-Adaptive Latent Upsampling (RALU)」を提案しています。既存の高速化手法が時間次元に焦点を当てる中、空間次元におけるエイリアシングやノイズ・タイムステップのミスマッチといったアーティファクトを抑制することが課題でした。RALUは、低解像度でのノイズ除去、エッジ領域の適応的アップサンプリング、最終的な詳細化のための全ラテントの高解像度アップサンプリングという3段階の混合解像度サンプリングを実行します。解像度移行時の安定化には、ノイズ・タイムステップ再スケジュールを活用します。実験では、FLUXで最大7.0倍、Stable Diffusion 3で3.0倍の高速化を達成し、画質劣化は最小限に抑えられました。本手法は既存の時間次元高速化手法とも併用可能です。

## 本研究の概要
本研究の目的は、Diffusion Transformers (DiTs) が高忠実度画像・動画生成において優れたスケーラビリティを持つ一方で、その高い計算コストがリアルワールドでの展開を妨げているという課題を解決することです。既存の高速化手法は主に時間次元（例：キャッシュ利用）に焦点を当てており、空間次元（例：低解像度処理）の高速化は未開拓でした。しかし、空間次元の高速化に伴う潜在表現のアップサンプリングでは、エッジ領域でのエイリアシングアーティファクトや、ノイズレベルとタイムステップの不整合によるミスマッチアーティファクトが発生するという問題がありました。

本研究では、これらの課題に対し、「Region-Adaptive Latent Upsampling (RALU)」という学習不要なフレームワークを提案することで解決を図りました。RALUは、まず低解像度で大域的なセマンティック構造を効率的に捉え、次にアーティファクトが発生しやすいエッジ領域を特定して適応的に高解像度化し、最後に残りの全ラテントを高解像度化して詳細を洗練するという3段階のプロセスを採用します。解像度移行時の安定化のためには、ノイズ・タイムステップ再スケジュール戦略を導入しました。この結果、FLUXモデルで最大7.0倍、Stable Diffusion 3モデルで最大3.0倍の高速化を達成し、画像品質の劣化は最小限に抑えることに成功しました。さらに、RALUは既存の時間次元高速化手法（例：キャッシュベースの手法）とも相補的であり、シームレスに統合することでさらなる推論レイテンシの削減が可能であることを示しました。

## 本研究の新規性や貢献
Diffusion Transformers (DiTs) は、高忠実度な画像・動画生成において最先端の性能を示しますが、特に高解像度での生成において、自己注意機構の計算コストが空間トークン数に対して二次的に増加するため、高い推論レイテンシが大きな課題となっています。この問題に対する先行研究は、主にモデル圧縮や時間次元（denoising timestep間での特徴再利用など）の高速化に焦点を当ててきました [29, 31, 8, 54]。一方で、空間次元（潜在表現の解像度を下げてトークン数を削減）の高速化は、「underexplored」な領域でした [46]。

既存の空間次元高速化の試みとしては、低解像度から高解像度へ段階的に画像を生成する「カスケード拡散フレームワーク」がありますが [39, 17, 45, 21]、これらは「training, which requires substantial resources」を必要とします。唯一の「training-free」な空間次元高速化手法であった「Bottleneck Sampling [46]」は、潜在アップサンプリング時に「artifacts caused by latent upsampling」に悩まされていました。具体的には、「aliasing artifacts that occur near edge regions」と「mismatching artifacts that were caused by inconsistencies in noise level and timestep」が発生するという問題がありました。

本研究は、これらの先行研究の限界を克服し、学習不要な形で空間次元の高速化を実現する点に新規性があります。主な貢献は以下の通りです。
1.  **領域適応型潜在アップサンプリング戦略（RALU）の提案**: 「progressively upsamples while prioritizing edge regions to suppress upsampling artifacts.」これにより、アーティファクトが発生しやすいエッジ領域に焦点を当てることで、効率的にエイリアシングアーティファクトを抑制します。
2.  **ノイズ・タイムステップ再スケジュールと分布マッチング（NT-DM）の導入**: 「stabilizes mixed-resolution sampling by aligning the noise level and timestep scheduling, and also allows RALU to be integrated with caching-based technique for additional speed-up.」これにより、ノイズレベルとタイムステップの不整合によるミスマッチアーティファクトを解決します。
3.  **優れた高速化と品質保持**: 「achieves up to 7.0 × speed-up on FLUX and 3.0 × on Stable Diffusion 3, with negligible degradation in generation quality.」競合する時間次元および空間次元の高速化手法と比較して、大幅な高速化と高品質な画像生成を両立できることを示しました。

## 手法
本研究は、Diffusion Transformersの推論を空間次元で高速化するため、学習不要な3段階の混合解像度サンプリングフレームワークである「Region-Adaptive Latent Upsampling (RALU)」を提案しています。また、解像度移行時のアーティファクトを抑制するため、「Noise-Timestep rescheduling with Distribution Matching (NT-DM)」を導入しています。

**RALUの3段階プロセス**:
1.  **低解像度でのノイズ除去 (Stage 1)**: 生成プロセスはまず低解像度で開始され、ノイズ除去を高速化します。「The generation process begins at the lower resolution to accelerate denoising. We reduce the latent resolution by a factor of 2 along both spatial dimensions (i.e., width and height), resulting in only 1/4 the number of latent tokens.」これにより、グローバルなセマンティック構造を効率的に捉えます。
2.  **エッジ領域のアップサンプリング (Stage 2)**: 潜在アップサンプリングは特にエッジ領域でエイリアシングアーティファクトを引き起こすため、これらの領域のラテントを選択的にアップサンプリングします。エッジ領域を特定するために、「we first estimate the clean latent x0 from the final latent of Stage 1 using Tweedie’s formula. This latent is then decoded into an image using the VAE decoder and apply Canny edge detection to locate structural boundaries. Next, we select the top-k latent patches corresponding to edge-dense regions (Fig. 3 (a)) and upsample them to a high-resolution( Fig. 3 (b)).」この解像度移行時には、ノイズ分布の変化に対応するため、後述のNT-DMを適用します。
3.  **全ラテントの高解像度化 (Stage 3)**: 最終段階では、残りの全ての低解像度ラテントトークンが高解像度にアップサンプリングされ、完全な高解像度画像を生成します。

**Noise-Timestep rescheduling with Distribution Matching (NT-DM)**:
学習不要な方法でアップサンプリングを行う際、ノイズとタイムステップのミスマッチアーティファクトが発生します。これを防ぐため、NT-DMは以下の2つの側面でノイズレベルとタイムステップを調整します。
*   **ノイズ注入**: アップサンプリング後の潜在空間の分布が元の軌道（rectified flow trajectory）から外れるため、「appropriate rescheduling noise z∼ N(0,Σ′)must be added to put back onto the rectified flow trajectory」。これにより、数式(6)に示すように、次ステージの開始タイムステップsk+1やノイズ注入の強さa, bが決定されます。
*   **タイムステップ再スケジュールと分布マッチング**: ノイズ注入後、拡散プロセスは新しいタイムステップsk+1から再開するため、元のモデルのタイムステップスケジュールをそのまま使用すると、重複する区間[sk+1, ek]でオーバーサンプリングが発生し、ミスマッチアーティファクトが生じます。NT-DMは、「it is critical to preserve the original model’s timestep distribution」。元のモデルのターゲット分布Ptarget(t) (数式8) と、実際のサンプリング分布P(t) (数式9) のJensen-Shannon divergence (JSD) を最小化するように、各区間のシフトパラメータ{hk}とノイズ注入の強さcを数値的に探索して決定します。

この3段階のプログレッシブな処理とNT-DMの組み合わせにより、「By progressively refining only the regions that are most vulnerable to upsampling artifacts and deferring full-resolution processing to the final stage, our three-stage method achieves substantial inference speedups while preserving high perceptual quality with negligible aliasing artifacts.」

## 評価方法と結果
本研究では、提案手法RALUの性能を評価するため、Flow MatchingベースのDiffusion TransformerであるFLUX.1-dev [1] とStable Diffusion 3 (SD3) [34] をベースモデルとして使用しました。

**評価方法**:
*   **メトリクス**: 画像品質はFID [15]、NIQE [32]、CLIP-IQA [47] で評価し、テキストアライメントはT2I-CompBench [20] とGenEval [13] で評価しました。高速化の度合いはレイテンシ（秒）、TFLOPs、およびスピードアップ倍率で定量化しました。
*   **比較対象**: 既存の時間次元高速化手法であるToCa [54] およびRAS [28]、そして空間次元高速化手法であるBottleneck Sampling [46] と比較しました。
*   **実験設定**: GenEvalでは553のプロンプトから2,212枚の画像を、T2I-CompBenchでは300のプロンプトから2,400枚の画像を生成し、評価を行いました。

**得られた結果**:
*   **T2I生成性能比較**:
    *   **FLUXモデル**: RALUは「up to 7.0 × speed-up on FLUX」を達成し、ベースライン（50ステップ）に比べて画質（FID: 30.07→28.68）とテキストアライメント（GenEval: 0.665→0.646）の劣化を最小限に抑えました（表1）。ToCaは画質とテキストアライメントで大幅な劣化を示し（FID: 51.83、GenEval: 0.509 at 4x）、Bottleneck Samplingはテキストアライメントは匹敵するものの、画質でRALUに劣りました（FID: 38.16 at 7x）。
    *   **SD3モデル**: RALUは「3.0 × on Stable Diffusion 3」の高速化を達成し、ここでも画質とテキストアライメントを堅牢に維持しました（表2）。
*   **キャッシングベース手法との統合**: RALUは既存のキャッシングベースの時間次元高速化手法と相補的であることを示しました。FLUXにおいて、RALU単独での4.13倍速化がキャッシングと統合することで「5.00 ×」に、7.02倍速化が「7.94 ×」に向上し、画質とテキストアライメントの劣化は最小限に抑えられました（表3）。
*   **アブレーションスタディ**:
    *   **NT-DMの効果**: タイムステップ分布P(t)とターゲット分布Ptarget(t)のJensen-Shannon divergence (JSD) を最小化するように決定された{hk}とcの値が、「Overall, selecting {hk} and c to minimize JSD performed better than other cases.」画像品質とテキストアライメントのメトリクスが向上することを示しました（表4）。
    *   **アップサンプリング比率の効果**: Stage 2におけるトップ-kラテントのアップサンプリング比率が高いほどテキストアライメントが改善されるが、FLOPsが増加するというトレードオフが確認されました（図6）。

**結果の解釈と考察**:
*   RALUは、他の高速化手法がしばしば「visible artifacts such as blurred edges, texture distortions and semantic inconsistencies」を導入するのに対し、「preserves structural fidelity and semantic details across acceleration levels」。特に高倍率の高速化においても、「RALU delivers the most visually faithful results.」
*   RALUが既存の時間次元高速化手法とシームレスに統合できることで、「additional efficiency gains with minimal degradation in quality」を実現可能であると結論付けられています。

## 制限事項と課題
本研究で提案されたRegion-Adaptive Latent Upsampling (RALU) は、Diffusion Transformersの推論高速化に効果的であることを示しましたが、いくつかの制限事項と今後の研究課題があります。

第一に、中核的な要素である「Noise-Timestep rescheduling with Distribution Matching (NT-DM)」は、「tailored specifically for flow-matching-based models.」であり、「Its effectiveness in other generative frameworks, such as score-based or DDIM-style diffusion, remains unverified.」このため、異なる拡散モデルの枠組み（スコアベース拡散モデルやDDIMスタイル拡散モデルなど）へのRALUの適用可能性は、今後の検証が必要となります。

第二に、RALUの汎化性に関する課題があります。「Moreover, generalization to other architectures or modalities (e.g., audio or 3D) remains unexplored, and further investigation is required to extend the applicability of RALU beyond current T2I generation.」現在の研究はテキスト・トゥ・イメージ（T2I）生成に特化しており、オーディオや3Dコンテンツ生成といった他のモダリティや、DiT以外のモデルアーキテクチャへの適用については、さらなる研究が必要とされています。

最後に、広範な影響（Broader Impact）に関する課題も認識されています。RALUによる効率化は、高品質な画像生成をより高速かつリソース効率的に可能にし、創造的なツールの民主化や環境コスト削減に貢献する可能性があります。しかし、「this efficiency gain may also facilitate misuse, such as faster generation of harmful or misleading content.」また、視覚的に顕著な領域（エッジなど）への選択的な焦点が、「implicitly encode or reinforce dataset biases, especially in underrepresented object structures.」を引き起こす可能性も指摘されています。論文では、「Care must be taken to evaluate fairness and misuse risks, and we encourage future work to explore responsible deployment strategies alongside technical improvements.」と述べられており、技術的改善と並行して、公平性や悪用リスクの評価、責任ある展開戦略の探求が今後の重要な課題として挙げられています。

---

*このファイルは自動生成されました。生成日時: 2025年07月23日 08:35:31*
