# MOSPA: Human Motion Generation Driven by Spatial Audio

**arXiv ID**: [2507.11949](http://arxiv.org/abs/2507.11949v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2507.11949v1.pdf)
**著者**: Shuyang Xu, Zhiyang Dou, Mingyi Shi, Liang Pan, Leo Ho, Jingbo Wang, Yuan Liu, Cheng Lin, Yuexin Ma, Wenping Wang, Taku Komura
**カテゴリ**: cs.GR, cs.CV, cs.RO
**公開日**: 2025-07-16T06:33:11Z

---

## 要約

## ショートサマリ
本研究は、仮想人間が多様な音響刺激、特に空間音声（spatial audio）に動的かつ現実的に反応するモーション生成の課題に取り組んでいます。従来のモデルは、空間音声に存在する空間的特徴を看過していました。この課題を解決するため、本研究は「Spatial Audio-Driven Human Motion (SAM) データセット」を世界で初めて構築しました。さらに、このデータセットに基づき、「human MOtion generation driven by SPatial Audio (MOSPA)」と名付けた、シンプルかつ効果的な拡散モデルベースの生成フレームワークを開発しました。MOSPAは、身体モーションと空間音声の関係を効果的な融合メカニズムを通じて忠実に捉えます。広範な実験により、MOSPAがこのタスクにおいて最先端（state-of-the-art, SOTA）の性能を達成することが示されました。

## 本研究の概要
本研究の目的は、キャラクターアニメーションにおいて、仮想人間が多様な音響刺激に対して動的かつ現実的に応答するモーションを生成することです。特に、従来の多くの研究がスピーチ、オーディオ、音楽といったモダリティからのモーション生成に焦点を当てていた一方で、空間音声（spatial audio）信号に符号化された空間的特徴が人間のモーションに与える影響は、これまでほとんど未探索のままでした。

本研究は、このギャップを埋めるために以下の成果を達成しました。第一に、多様で高品質な空間音声とモーションデータを含む、初の包括的な「Spatial Audio-Driven Human Motion (SAM) データセット」を構築しました。このデータセットは9時間以上のモーションデータを含んでいます。第二に、このデータセットのベンチマーク設定のために、「MOSPA（MOtion generation driven by SPatial Audio）」と名付けた、シンプルかつ効果的な拡散モデルベースの生成フレームワークを開発しました。MOSPAは、効果的な融合メカニズムを通じて、身体モーションと空間音声の間の関係を忠実に捉えることができます。一度訓練されると、MOSPAは様々な空間音声入力に基づいて、多様で現実的な人間のモーションを生成することが可能になります。広範なベンチマーク実験により、我々の手法がこのタスクにおいて最先端の性能を達成したことを示しました。

## 本研究の新規性や貢献
本研究は、仮想人間が多様な音響刺激に動的かつ現実的に応答するモーション生成における、未開拓の課題に焦点を当てています。これまでの研究は、スピーチ、オーディオ、音楽といった一般的な音響から人間モーションを生成することに注力していましたが、空間音声（spatial audio）に含まれる空間的特徴が身体の動きに与える影響は、これまでほとんど見過ごされていました。空間音声は、単なる意味だけでなく、音源の方向や距離といった空間的特性もエンコードしており、これらを正確にモデル化するには専用のフレームワークが必要です。

この未開拓の側面に対処するため、本研究は以下の主要な貢献をしています。
- まず、「空間音声条件付きモーション生成」という新しいタスクを導入し、これに対応する初の包括的なデータセット「SAM（Spatial Audio-Driven Human Motion）データセット」を構築しました。このデータセットは、多様なシナリオにわたる9時間以上のモーションを含んでいます。
- 次に、この新しいタスクに特化し、空間音声から多様な人間モーションをモデリングおよび生成するための拡散モデルベースの生成フレームワーク「MOSPA」を提案しました。
- 最後に、MOSPAが空間音声条件付きモーション生成において、既存のベースライン手法を上回り、最先端（SOTA）の性能を達成したことを実証しました。我々のデータセット、コード、モデルは、今後の研究のために公開される予定です。

## 手法
MOSPAは、空間音声駆動型人間モーション生成のための拡散モデルベースの確率的モデルです。このモデルは、空間音声から抽出された特徴量、音源位置（SSL）、およびモーションジャンルを条件付け入力として使用します。

主要な要素は以下の通りです。
- **空間音声特徴抽出**: 音響の強度、時間ダイナミクス、空間特性を捉えるために、様々なオーディオ特徴を抽出します。これには、「Mel-frequency cepstral coefficients (MFCC)」、「MFCC delta」、「constant-Q chromagram」、「short-time Fourier transform (STFT) of the chromagram」、「onset strength」、「tempogram」、「beats」が含まれます。さらに、オーディオの距離情報を捉えるために、「root mean square (RMS) energy」と「active frames」が追加されます。「By concatenating the features from both ears, we obtain a combined feature vector a of dimension 2272.」
- **モーション表現**: 人間モーションは、SMPL-Xモデルの25の身体関節の情報を基に表現されます。「Each motion vector x is thus composed of the global positions p∈RT×(J×3), the local rotations r∈RT×(J×6) and the velocities v∈RT×(J×3) of the joints (including the root), where T= 240 represents the number of frames in each motion sequence. The joint rotations are represented in the 6d format [98] to guarantee the continuity of the change (x0= (p0,r0,v0),x∈RT×(J×12)). The dimension of each motion vector is therefore 300.」
- **フレームワーク**: 拡散プロセスは、エンコーダのみのTransformerモデルによって逆転されます。このモデルは、ノイズの多いモーションベクトル `xt` から元のクリーンなモーション `ˆx0` を予測するように訓練されます。「We directly predict the clean sample ˆx0 in each diffusion step ˆx0=G(xt, t;a,s, g), where a is the audio features, s is the sound source location and g is the motion genre.」
- **損失関数**: 主目的は平均二乗誤差（MSE）損失「Ldata =E∥ˆx0−x0∥22+E∥δˆx0−δx0∥22」であり、これに幾何学的損失「Lgeo」、足接触損失「Lfoot」、軌道損失「Ltraj」、関節回転損失「Lrot」を組み合わせた合計損失「L=λdataLdata+λgeoLgeo+λfootLfoot+λtrajLtraj+λrotLrot (2)」が用いられます。

## 評価方法と結果
本研究では、提案手法MOSPAの評価のために、SAMデータセットを用いた広範な実験とユーザー調査を行いました。

**実験・評価方法**:
- **データセット**: SAMデータセットを訓練、検証、テストに8:1:1の比率で分割し、それぞれ2,400、300、300のモーションシーケンスを使用しました。
- **ベースライン**: 既存のaudio2motion手法であるEDGE [75]、POPDG [57]、LODGE [45]、Bailando [68]を空間音声入力に対応するよう適応させて比較しました。
- **評価指標**: モーション品質と多様性を評価するため、「R-precision」、「FID（Fréchet Inception Distance）」、「Diversity」、「APD（Average Pose Distance）」の4つの指標を使用しました。「We evaluated four metrics, focusing on motion quality and diversity: 1)R-precision, FID, Diversity... 2)APD [18,32]...」
- **ユーザースタディ**: 25名の参加者がMOSPAを含む5つのモデルとグラウンドトゥルース（GT）を比較し、「人間の意図との整合性」、「モーション品質」、「GTとの類似性」の3つの基準で最も良いモーションを選択しました。
- **アブレーションスタディ**: モデルの潜在次元数、Attention Head数、拡散ステップ数、モーションジャンルマスキングが性能に与える影響を分析しました。

**得られた結果と考察**:
- **定量的結果**: MOSPAは、最も低いFID値（7.981）と最も高いR-precision値（Top1で0.937）を達成し、最先端の性能を示しました。「MOSPA achieves the best performance as shown by the lowest FID value and the highest R-precision values. Also, our generated motions exhibit the closest diversity and APD [18] values compared with the Real Motion, demonstrating the effectively balanced variation and precision.」
- **定性的結果とユーザースタディ**: MOSPAは、高品質で現実的な応答モーションを生成し、ユーザースタディにおいてもすべての基準で他のベースラインを上回りました。「MOSPA (Ours) outperforms all baselines across all criteria」他のベースラインモデルは、主に音楽やスピーチに特化しているため、空間音声の急激な変化や空間情報を処理する際に限界が見られました。特にBailandoは、空間音声の急激な変化に際して歪んだモーションを生成する傾向がありました。
- **アブレーションスタディ**: 潜在次元数、Attention Head数、拡散ステップ数の削減は性能の低下を招きました。また、モーションジャンルのマスキングもモデル性能を低下させ、「Motion genres are required to provide a guidance for the model on the intensity of the expected motions.」と結論付けられました。

## 制限事項と課題
本研究にはいくつかの制限事項があり、これらは今後の研究課題として挙げられています。

- **物理的正確性**: 「While MOSPA generates diverse and semantically plausible motions, it lacks physical constraints, which may lead to physically implausible artifacts.（MOSPAは多様で意味的に妥当なモーションを生成するものの、物理的な制約を欠いているため、物理的にありえないアーティファクトが発生する可能性がある。）」今後の研究では、物理ベースの制御手法[18,56,73,37,92,93,59,79]を統合することで、モーションのリアリズムと具現化の忠実度を向上できる可能性があります。

- **身体モデリング**: 「This work focuses on body motion and omits finer-grained components such as hand gestures and facial expressions supported by SMPL-X [60].（本研究は身体の動きに焦点を当てており、SMPL-X [60]でサポートされている手のジェスチャーや顔の表情のようなよりきめ細かい要素は省略している。）」将来の研究では、モデルを全身モーション生成[54,49,83,61,5]（手の動きを含む）に拡張することが重要な方向性となります。

- **シーン認識**: 「The current framework does not incorporate awareness of surrounding environments or physical scene geometry, limiting its ability to produce scene-consistent or contact-aware motions.（現在のフレームワークは、周囲の環境や物理的なシーンのジオメトリの認識を組み込んでいないため、シーンに一貫したモーションや接触を考慮したモーションを生成する能力が限られている。）」今後の拡張では、シーン表現やアフォーダンス予測[13,78,80,7,77]を空間音声信号と統合することで、人間モーション生成を強化できる可能性があります。

---

*このファイルは自動生成されました。生成日時: 2025年07月17日 08:33:51*
