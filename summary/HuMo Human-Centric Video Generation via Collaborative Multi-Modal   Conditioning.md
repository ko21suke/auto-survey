# HuMo: Human-Centric Video Generation via Collaborative Multi-Modal   Conditioning

**arXiv ID**: [2509.08519](http://arxiv.org/abs/2509.08519v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2509.08519v1.pdf)
**著者**: Liyang Chen, Tianxiang Ma, Jiawei Liu, Bingchuan Li, Zhuowei Chen, Lijie Liu, Xu He, Gen Li, Qian He, Zhiyong Wu
**カテゴリ**: cs.CV, cs.MM
**公開日**: 2025-09-10T11:54:29Z

---

## 要約

##0ショートサマリ
本研究は、人物中心の動画生成（HCVG）における、テキスト・画像・音声といった異種モダリティの協調制御の難しさ、特に訓練データの不足と被写体維持および視聴覚同期サブタスクの連携問題を解決します。HuMoは、高品質なマルチモーダルデータセットの構築、タスク固有の戦略（最小侵襲型画像注入、予測によるフォーカス）を用いた2段階の漸進的トレーニングパラダイム、および時間適応型Classifier-Free Guidance（CFG）戦略を導入することで、これらの課題に対処しました。実験結果は、HuMoがサブタスクにおいて既存の最先端手法を上回り、統一された協調的なマルチモーダル条件付きHCVGフレームワークを確立したことを示しています。

##1本研究の概要
人物中心の動画生成（HCVG）は、テキスト、画像、音声といったマルチモーダル入力から人物動画を合成する技術ですが、既存手法ではこれら異種モダリティを効果的に連携させることが困難でした。具体的な課題は、「ペアになった3種類の条件を持つ訓練データの不足（the scarcity of training data with paired triplet conditions）」と、「マルチモーダル入力を用いた被写体維持と視聴覚同期サブタスクの協調の難しさ（the difficulty of collaborating the sub-tasks of subject preservation and audio-visual sync with multimodal inputs）」です。

本研究は、これらの課題を克服し、協調的なマルチモーダル制御を可能にする統一HCVGフレームワーク「HuMo」を提案しました。HuMoは、高品質で多様なペアのテキスト、参照画像、音声データセットを構築し、タスク固有の戦略（被写体維持のための「最小侵襲型画像注入」、視聴覚同期のための「予測によるフォーカス」）を用いた2段階の漸進的なマルチモーダルトレーニングパラダイムを採用しました。さらに、推論時には、ノイズ除去ステップ全体でガイダンス重みを動的に調整する時間適応型Classifier-Free Guidance戦略を設計し、柔軟できめ細やかなマルチモーダル制御を実現しました。これにより、HuMoは被写体維持と視聴覚同期の両サブタスクにおいて最先端の手法を上回る性能を示し、統一された協調的なHCVGフレームワークを確立しました。

##2本研究の新規性や貢献
本研究の背景には、人物中心の動画生成（HCVG）におけるマルチモーダル制御の不均衡という課題があります。現在のHCVG手法は、テキスト、画像、音声といった異種モダリティを効果的に協調させることに苦慮しており、特に「ペアになった3種類の条件を持つ訓練データの不足（Data scarcity）」と、「マルチタスク学習フレームワーク内での協調的なマルチモーダル制御の難しさ（Difficulty in collaborative multimodal control）」が主要な課題として挙げられます。

関連する先行研究にはいくつかの限界がありました。例えば、従来のHCVG手法はテキストから画像への生成（T2I）と画像から動画への生成（I2V）の2段階パイプラインを採用していましたが、これは開始フレームに大きく依存し、「テキスト制御の柔軟性を本質的に制約（inherently constrains the flexibility of text controls）」していました。また、被写体一貫性動画生成（S2V）手法は参照画像とテキストによる動画カスタマイズを可能にしましたが、「音声モダリティを組み込むことができず、キャラクターの発話を制御できません（unable to incorporate an audio modality and cannot control what a character is speaking）」。最近の統合を試みる手法も、「テキスト、参照画像、音声の3つの入力モダリティ間で効果的な協調を達成するのに苦労（struggle to achieve effective collaboration among the triplet input modalities of text, reference images, and audio）」していました。例えば、参照画像の影響を強調すると視聴覚同期が低下し、同期を優先するとテキスト追従性や被写体維持能力が損なわれる傾向がありました。

本研究は、このような既存手法の限界を乗り越えるため、「データ処理パイプラインとトレーニングパラダイムにわたる包括的な設計が不足しているため、既存のHCVG手法におけるマルチモーダル制御の不均衡が生じている（attribute the imbalanced multimodal controllability in existing HCVG methods to the absence of a comprehensive design across data processing and training paradigms for handling heterogeneous inputs）」という概念を提唱し、HuMoを提案します。HuMoは、テキスト、画像、音声のモダリティ間で協調的な制御を可能にする統一フレームワークとして位置づけられます。

##3手法
本研究では、DiTベースのテキスト-動画（T2V）モデル[31]をバックボーンとして拡張し、画像と音声の追加モダリティを組み込んだHuMoフレームワークを提案します。モデルはフローマッチング[20]に基づき、ノイズからデータ分布への連続的な速度場を学習します。

**マルチモーダルデータ処理パイプライン**
高品質なマルチモーダルデータセットを構築するため、2段階のパイプラインを採用しています。
1.  **ステージ1**: 大規模動画プール[18,33]から、VLMs[1,30]でテキスト記述を生成します。その後、「大規模画像コーパスから、動画サンプル中の各被写体について、同じ意味だが異なる視覚属性を持つ参照画像を検索（retrieve reference images with the same semantics but different visual attributes [3,22] for each subject in the video samples from a billion-scale image corpus）」します。
2.  **ステージ2**: 音声同期動画生成のため、「音声強調とリップアライメント推定[17]を用いて、同期された音声トラックを持つ動画サンプルをさらにフィルタリング（filter video samples with synchronized audio tracks using speech enhancement and speech-lip alignment estimation [17]）」します。

**漸進的なマルチモーダルトレーニング**
マルチモーダル制御能力の獲得を2つの漸進的なトレーニングステージで構成します。
1.  **ステージ1（被写体維持タスク）**: テキストと画像の協調制御を確立します。DiTバックボーンのテキスト追従能力と画像生成能力を維持するため、「最小侵襲型画像注入戦略（minimal-invasive image injection strategy）」を採用します。具体的には、「参照画像のVAEラテントをノイズ入りラテントと時間次元に沿って結合（concatenate the VAE latents zimg of the reference images cimg with the noisy latent zt along the temporal dimension as inputs）」し、参照ラテントを動画ラテントシーケンスの最後に配置します。トレーニングはDiTの自己注意層に限定されます。
2.  **ステージ2（視聴覚同期タスク）**: 音声モダリティを導入します。各DiTブロックに音声クロスアテンション層を挿入し、Whisper[26]で音声特徴を抽出します。音声が顔領域と最も相関するという観察に基づき、「モデルが顔領域と音声を関連付けるよう暗黙的に誘導する予測によるフォーカス戦略（focus-by-predicting strategy that implicitly guides the model to associate audio with facial regions）」を提案します。これは、マスク予測器`F_mask`を導入し、顔領域分布`M_pred`を推定し、グラウンドトゥルースのバイナリ顔マスク`M_gt`で二値交差エントロピー（BCE）損失を用いて教師あり学習を行うものです。この戦略は、「モデルの表現能力を損なうことなく焦点を誘導するソフトな正則化として機能（acts as a soft regularizer, which steers the model’s focus without crippling its representational capacity）」します。
    「被写体維持能力が損なわれないように、ステージ2では初期は被写体維持タスクが主（80%）、視聴覚同期タスクが従（20%）で、トレーニングが進むにつれて視聴覚同期タスクの割合を徐々に50%に増やします（Initially, training is dominated by the subject preservation task (80% ratio, audio input as null) ..., while the audio-visual sync task constitutes the remaining 20%. As training progresses, we gradually increase the proportion of the audio-visual sync task to 50%.）」。

**推論戦略**
柔軟なマルチモーダル制御のため、「時間適応型Classifier-Free Guidance（CFG）戦略（time-adaptive Classifier-Free Guidance (CFG) strategy）」を提案します。これは、ノイズ除去ステップ全体でガイダンス重みを動的に調整するもので、「早期ステップでは全体的な意味構造と空間レイアウトを構築し、後期ステップではきめ細やかな詳細に焦点を当てる（early steps tend to construct the overall semantic structure and spatial layout guided by text, while later steps focus on fine-grained details）」という観察に基づいています。

##4評価方法と結果
本研究では、Wan-2.1-1.3BおよびWan-2.1-14B[31]をバックボーンとしてHuMoを構築し、2段階のトレーニング戦略を採用しました。比較対象として、S2V（Subject-to-Video generation）手法（MAGREF[7]、HunyuanCustom[11]、Phantom-Wan-14B[22]、Kling 1.6[14]）と、視聴覚同期手法（Hallo3[5]、FantasyTalking[32]、HunyuanCustom[11]、OmniHuman-1[19]）を用い、それぞれ自社ベンチマークおよびMoChaベンチマーク[35]で評価しました。

評価には以下の4つの主要側面をカバーする客観的指標を使用しました。
1.  **動画品質**: VBench[13]による美学（AES）と画質評価（IQA）、およびGemini-2.5-Pro[30]による人間構造の妥当性（HSP）。
2.  **テキスト-動画アライメント（TVA）**: VLMベースの報酬モデル[21]によるセマンティック一貫性。
3.  **被写体一貫性**: 顔についてはFace-Cur[12]とFace-Glink[6]、非顔オブジェクトについてはDINO-I[23]とCLIP-I[25]スコア。
4.  **視聴覚同期**: Sync-CおよびSync-D[17]による音声と顔の動きのアライメント。

**結果の概要と解釈**:
**被写体維持タスク**: 定性的には、HuMoは「他の手法と比較してテキスト追従能力に優れている（HuMo demonstrates superior performance in text following ability compared to other methods）」ことが示されました。特に図5のケース(b)では、他の手法が「step into a temple」の生成に失敗する中、HuMoは4つの異なる人物のアイデンティティを正確に維持しました。定量的には、Table 1より「HuMoは美的および全体的な画質において他の手法を上回る（HuMo outperforms other methods in aesthetic and overall image fidelity）」結果を示し、最高のHSPスコアで人間ポーズと身体完全性のモデリングにおいて強力な能力を達成しました。本研究は、「参照画像とのテキスト追従性および被写体一貫性においてもSOTA性能を達成（HuMo also achieves the SOTA performance, which is consistent with the qualitative observation）」しており、テキスト編集性と被写体一貫性を両立できることを示しています。

**視聴覚同期タスク**: 定性的には、図6よりHuMoの「テキスト追従能力の優位性（HuMo’s superior capability in text following）」が明らかになりました。ケース(a)と(c)では、「silver guitar」や「golden light in the background」といった詳細を成功裏に合成しており、これは「I2Vベースの手法の根本的な弱点である、提供された被写体完全な開始フレームを再編集する能力の限界（fundamental weakness of I2V-based methods - their limited ability for re-editing the provided subject-complete start frame）」をHuMoが克服したことを示唆しています。定量的には、Table 2より「HuMoは美的品質とテキスト追従性において最高のスコアを達成（HuMo attains the highese scores for aesthetic quality and text follwing）」しました。視聴覚同期においても、「1.7Bモデルでさえいくつかのオープンソースの専門モデルをすでに上回り、商用手法であるOmniHuman-1にわずかに劣るのみ（our 1.7B model already outperforms several open-source specialized models and trails only slightly behind the commercial method OmniHuman-1）」でした。これは、本研究のモデルが、ボディレイアウトや顔の構造に関する強力な事前知識を持つI2Vベースの手法と比較しても遜色ない性能を示すことを強調しています。

##5制限事項と課題
本研究の主要な制限事項および課題は、「Ethical Considerations」セクションで言及されている倫理的な懸念です。論文では、「HuMoの開発は、いくつかの倫理的懸念を引き起こす可能性がある（The development of HuMo for Human-Centric Video Generation may raise several ethical concerns）」と指摘されています。

具体的には、第一に、「マルチモーダル入力（テキスト、画像、音声）からリアルな人間動画を合成する能力は、ディープフェイクや非同意のコンテンツ作成などの悪用につながる可能性がある（the ability to synthesize realistic human videos from multimodal inputs (text, image, and audio) may lead to misuse, such as deepfakes or non-consensual content creation）」と述べられています。この問題は、リアルな人間中心の動画生成技術が持つ潜在的なリスクとして、今後の研究や社会的な議論で対処されるべき重要な課題です。

第二に、「生成されるコンテンツに対するきめ細かな制御は、操作や誤報を防ぐための責任ある利用ガイドラインを求めている（fine-grained control over generated content calls for responsible usage guidelines to prevent manipulation or misinformation）」とされています。この点は、技術の高度化に伴い、その利用方法に対する倫理的・社会的な責任がますます重要になることを示唆しています。

今後の研究課題や展望としては、「情報に基づいた同意を確保し、個人の肖像権を保護することが極めて重要である（Ensuring informed consent and protecting individuals’ likenesses are critical）」とされており、技術開発と並行して、これらの倫理的側面への配慮が不可欠であると結論付けられています。また、「開発者とユーザーは、透明性、データプライバシー、危害の防止を含む倫理的基準を遵守しなければならない（Developers and users must adhere to ethical standards, including transparency, data privacy, and the prevention of harm）」とも述べられており、技術だけでなく、その運用に関わる全てのステークホルダーが負うべき責任が強調されています。

---

*このファイルは自動生成されました。生成日時: 2025年09月12日 08:27:55*
