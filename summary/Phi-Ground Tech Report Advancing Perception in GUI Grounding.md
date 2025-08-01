# Phi-Ground Tech Report: Advancing Perception in GUI Grounding

**arXiv ID**: [2507.23779](http://arxiv.org/abs/2507.23779v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2507.23779v1.pdf)
**著者**: Miaosen Zhang, Ziqiang Xu, Jialiang Zhu, Qi Dai, Kai Qiu, Yifan Yang, Chong Luo, Tianyi Chen, Justin Wagle, Tim Franklin, Baining Guo
**カテゴリ**: cs.CV, cs.AI, cs.MM
**公開日**: 2025-07-31T17:59:09Z

---

## 要約

## #0ショートサマリ
本研究は、CUA（Computer Use Agents）の中核技術であるGUI groundingの精度が低く、実用化を妨げている問題に取り組みました。この課題に対し、データ収集からモデル訓練までの詳細な経験的学習を実施し、Phi-Groundモデルファミリーを開発しました。本モデルは、モダリティ入力順序の最適化、データ拡張（Random Crop, Random Resize）、データ分布の再サンプリング、イン・ドメインの事後訓練（DPOなど）といった手法を統合しています。実験結果として、Phi-Groundはエージェント設定において、5つのGUI groundingベンチマーク全てで最先端（SOTA）の性能を達成し、特にScreenSpot-proで55.0、UI-Visionで36.2を記録しました。エンドツーエンドモデル設定でもScreenSpot-proで43.2、UI-Visionで27.2を達成し、高い汎化能力を示しました。

## #1本研究の概要
本研究の背景には、マルチモーダル推論モデルの発展に伴い、CUA（Computer Use Agents）が現実味を帯びてきたことがあります。CUAが実際のアクション（クリックやタイピング、座標決定など）を実行するためにはGUI groundingが不可欠ですが、既存のエンドツーエンドgroundingモデルは、ScreenSpot-proやUI-Visionといった挑戦的なベンチマークで「less than 65% accuracy」しか達成しておらず、実用には程遠い状態でした。本研究の目的は、このGUI groundingモデルの訓練に関する詳細な経験的研究を行い、性能を飛躍的に向上させることで、CUAの実用化を推進することでした。

本研究で達成できたことは多岐にわたります。まず、データ収集からモデル訓練までの詳細な経験的学習を通じて、効率的かつ合理的な訓練レシピを考案し、40M以上のデータサンプルを収集しました。これにより、Phi-Groundモデルファミリーを開発しました。このモデルファミリーは、エージェント設定（LLMが詳細な参照表現を生成する2段階アプローチ）において、10Bパラメータ未満のモデルとして5つのGUI groundingベンチマーク全てでSOTA性能を達成しました。特にScreenSpot-proでは55.0、UI-Visionでは36.2を記録しました。さらに、エンドツーエンドモデル設定においても、「scores of 43.2 on ScreenSpot-pro and 27.2 on UI-Vision」というSOTA結果を達成し、モデルの強力な汎化能力を示しました。本論文で議論された訓練の詳細、成功と失敗の経験が、groundingモデル構築だけでなく、他の知覚タスクにも貢献する可能性も示唆しています。

## #2本研究の新規性や貢献
本研究は、CUA（Computer Use Agents）の核となるGUI grounding技術の現状と課題を解決するものです。GUI groundingの精度は依然として低く、既存のエンドツーエンドモデルはScreenSpot-proやUI-Visionのような挑戦的なベンチマークで「less than 65% accuracy」に留まり、実用には不十分でした。また、先行研究における座標のトークン化、ラベルスムージング、損失の重み付けといった手法は、大規模訓練においてその利点が「become trivial when dealing with large-scale training」と判明しており、訓練のスケールアップに関する詳細な知見が不足していました。

本研究の新規性は、これらの課題に対し、GUI groundingモデルの訓練プロセス全体にわたる詳細な経験的学習を実施した点にあります。具体的には、モダリティ入力順序の最適化、高解像度シナリオにおけるデータ拡張（Random Resizeなど）の有効性の検証、データ分布の偏りを補正する再サンプリング技術の導入、そして特定シナリオでのin-domain継続学習におけるデータ戦略と強化学習（DPO）の有効性を示しました。さらに、モデルのパラメータ数だけでなく、推論時の計算負荷（画像トークン数）を考慮したスケーリング法則を研究しました。

これらの知見と最適化された訓練レシピにより、「Phi-Ground」モデルファミリーを開発し、エージェント設定およびエンドツーエンド設定の両方で複数のGUI groundingベンチマークにおいて最先端（SOTA）の性能を達成しました。本研究は、GUI groundingの性能を大幅に向上させるだけでなく、その訓練に関する実用的な指針を提供し、他のマルチモーダル知覚タスクへの応用可能性も示唆しており、CUAの実用化に向けた重要な貢献をしています。

## #3手法
本研究では、GUI groundingモデルの精度向上を目指し、大規模なデータ収集と訓練手法の最適化を通じて、Phi-Groundモデルファミリーを開発しました。

**研究のアプローチと方法論**:
本モデルは2段階アプローチを採用。まず、強力なMLLM（例：GPT-4O）が詳細な「参照表現（RE）」を生成し、次に訓練した小型MLLMがREに基づき画面座標をテキスト形式で直接出力します。

**特徴的な技術や手法の詳細**:
1.  **大規模データセットの構築と処理**:
    既存のオープンソースデータに加え、CommonCrawlのWebページレンダリングデータ、Bing Image Search APIによる高解像度画像、人手アノテーションデータを含む「over 40M data samples from multiple sources」を収集。ノイズ除去のため「highly specific data cleaning pipeline」を適用し、GPT-4Oによる詳細REで再アノテーションしました。データ内の要素中心点の偏りを是正するため、画像グリッドに基づく「re-sampling technique」も導入しました。

2.  **訓練手法の最適化**:
    *   **入力モダリティ順序**: テキスト情報を画像情報よりも先に入力することで、画像特徴の「instruction-aware」なモデリングを促し、性能が大幅に向上することを実証しました。「inputting text before images yields significantly better outcomes in the reverse order」。
    *   **データ拡張**: 高解像度シナリオでの小要素認識能力向上のため、「Random Resize」が特に有効であることを発見しました。「certain data augmentations can greatly enhance results in high-resolution scenarios (such as ScreenSpot-pro)」。
    *   **イン・ドメインの事後訓練**: 特定アプリケーションへの適応性を高めるため、事前訓練とSFT（Supervised Fine-Tuning）にドメインデータを組み込む戦略を最適化しました。さらに、DPO（Direct Preference Optimization）を複数ラウンド適用することで、純粋な知覚タスクにおいて「RL can consistently outperform SFT in purely perceptual tasks, even when starting from a highly optimized pre-trained checkpoint」と、最適化済みモデルの性能をさらに引き出す成果を得ました。

## #4評価方法と結果
本研究では、モデルの汎化能力を評価するため、ScreenSpot V1 & V2, ScreenSpot-Pro, UI-Vision, Showdown-click-devの公開ベンチマークと、独自構築のGoldデータセットを含む計5つの評価データセットを使用しました。主要な評価指標はクリック精度（Click Accuracy）です。参照表現（RE）は、ベンチマーク提供の「Short / instruction」と、MLLMが詳細を加えて拡張した「Long / agent」の2種類で評価しました。

**得られた結果の概要**:
Phi-Groundモデルファミリーは、以下の顕著な結果を達成しました。
*   **エージェント設定でSOTA性能**: Long REを使用するエージェント設定において、5つのGUI groundingベンチマーク全てで最先端（SOTA）の性能を達成。「our Phi-Ground model achieves state-of-the-art results across all benchmarks, with particularly high scores of 55.0 and 36.2 on ScreenSpot-pro and UI-Vision, respectively.」商用モデルも凌駕する結果を示しました。
*   **エンドツーエンド設定でSOTA性能**: Short REを使用するエンドツーエンドモデル設定でも、ScreenSpot-Pro、UI-Vision、GoldデータセットでSOTA結果を達成。「in the end-to-end model setting, our model still achieves SOTA results with scores of 43.2 on ScreenSpot-pro and 27.2 on UI-Vision.」
*   **汎化能力とスケーリング**: 複数ベンチマークでの一貫した高性能は、モデルの優れた汎化能力を示します。また、高解像度ベンチマークでは画像トークン数が性能に大きく影響するが、約2000を超えると限界利益が減少することが示唆されました。

**結果の解釈や考察**:
本モデルはAgent設定に特化して訓練され、この設定で顕著な優位性を示しました。訓練における各技術の慎重な選択とアブレーションが、モデルのバランスの取れた性能と優れた汎化能力に貢献しています。

## #5制限事項と課題
本研究はGUI groundingの進歩に貢献しましたが、CUAの実用化にはいくつかの制限事項と課題が残っています。

**研究の限界や未解決の問題**:
1.  **ユーザープライバシーと誤動作の責任**: CUAは機能上、ユーザー画面のスクリーンショットをクラウドにアップロードする可能性があり、プライバシー侵害のリスクがあります。「the need for grounding and planning may require screenshots of users’ screens to be uploaded to the cloud, potentially leading to privacy breaches.」また、CUAが取り返しのつかない有害な操作（例：ファイル削除）を実行する可能性や、groundingモデルの誤動作がインタラクティブな領域を誤って出力することによる深刻な影響が懸念されます。
2.  **言語および視覚的課題**: 訓練データが主に英語であるため、中国語などの非英語言語が含まれるUIの認識に問題が生じる場合があります。「the target area or its vicinity contained languages not covered by our model, such as Chinese.」さらに、極端な画面サイズ/形状や、自然言語で記述が困難な領域、複雑な空間計画を要するタスク（例：テーブルの特定セル）において、モデルの精度が低下する課題が残されています。

**今後の研究課題や展望**:
*   ユーザープライバシー保護のためのプロトコル、法的枠組み、またはアルゴリズムの確立が不可欠です。
*   人間とコンピューターの協調方法を探求し、人間の監視下でCUAが効率的に作業を代替できるシステムを構築する必要があります。
*   GUI groundingモデルの潜在的な有害性を評価するベンチマークの開発が、今後の研究に大きく貢献するでしょう。

---

*このファイルは自動生成されました。生成日時: 2025年08月01日 08:34:30*
