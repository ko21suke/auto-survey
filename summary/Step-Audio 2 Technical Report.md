# Step-Audio 2 Technical Report

**arXiv ID**: [2507.16632](http://arxiv.org/abs/2507.16632v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2507.16632v1.pdf)
**著者**: Boyong Wu, Chao Yan, Chen Hu, Cheng Yi, Chengli Feng, Fei Tian, Feiyu Shen, Gang Yu, Haoyang Zhang, Jingbei Li, Mingrui Chen, Peng Liu, Wang You, Xiangyu Tony Zhang, Xingyuan Li, Xuerui Yang, Yayue Deng, Yechang Huang, Yuxin Li, Yuxin Zhang, Zhao You, Brian Li, Changyi Wan, Hanpeng Hu, Jiangjie Zhen, Siyu Chen, Song Yuan, Xuelin Zhang, Yimin Jiang, Yu Zhou, Yuxiang Yang, Bingxin Li, Buyun Ma, Changhe Song, Dongqing Pang, Guoqiang Hu, Haiyang Sun, Kang An, Na Wang, Shuli Gao, Wei Ji, Wen Li, Wen Sun, Xuan Wen, Yong Ren, Yuankai Ma, Yufan Lu, Bin Wang, Bo Li, Changxin Miao, Che Liu, Chen Xu, Dapeng Shi, Dingyuan Hu, Donghang Wu, Enle Liu, Guanzhe Huang, Gulin Yan, Han Zhang, Hao Nie, Haonan Jia, Hongyu Zhou, Jianjian Sun, Jiaoren Wu, Jie Wu, Jie Yang, Jin Yang, Junzhe Lin, Kaixiang Li, Lei Yang, Liying Shi, Li Zhou, Longlong Gu, Ming Li, Mingliang Li, Mingxiao Li, Nan Wu, Qi Han, Qinyuan Tan, Shaoliang Pang, Shengjie Fan, Siqi Liu, Tiancheng Cao, Wanying Lu, Wenqing He, Wuxun Xie, Xu Zhao, Xueqi Li, Yanbo Yu, Yang Yang, Yi Liu, Yifan Lu, Yilei Wang, Yuanhao Ding, Yuanwei Liang, Yuanwei Lu, Yuchu Luo, Yuhe Yin, Yumeng Zhan, Yuxiang Zhang, Zidong Yang, Zixin Zhang, Binxing Jiao, Daxin Jiang, Heung-Yeung Shum, Jiansheng Chen, Jing Li, Xiangyu Zhang, Yibo Zhu
**カテゴリ**: cs.CL, cs.SD, eess.AS
**公開日**: 2025-07-22T14:23:55Z

---

## 要約

## ショートサマリ
本研究は、既存の大規模音声言語モデル（LALM）が抱えるパラ言語情報の無視、幻覚、音色の多様性不足といった課題を解決するため、エンドツーエンドのマルチモーダルLALMである「Step-Audio 2」を提案します。本モデルは、潜在音声エンコーダと推論中心の強化学習（RL）を統合し、さらに離散音声トークンの生成を言語モデリングに組み込むことで、真のエンドツーエンド音声会話を実現します。また、Retrieval-Augmented Generation (RAG)と外部ツール（ウェブ検索、音声検索など）を活用し、リアルワールドの知識と表現力を強化します。数百万時間の音声データで学習されたStep-Audio 2は、自動音声認識（ASR）、音声理解、音声翻訳、音声会話など、多様なベンチマークにおいて最先端の性能を達成しました。

## 本研究の概要
本研究の目的は、産業レベルの音声理解と音声会話のための、より自然で知的なエンドツーエンドのマルチモーダル大規模言語モデル（LLM）を開発することです。従来のLALMは、音声入力のセマンティック情報（意味内容）の整合に主眼を置き、「話し方や感情などのパラ言語情報」（paralinguistic information）を無視したり、出力がテキストに限定されたりする課題がありました。また、「マルチモーダルモデリングの複雑さ」により、「幻覚」（hallucination）の発生や「音色や話し方の選択肢の制限」という問題も抱えていました。

これらの課題を解決するため、本研究は「Step-Audio 2」を開発しました。Step-Audio 2は、生の音声を直接入力として処理し、離散的なテキストトークンと音声トークンを生成します。これにより、意味情報だけでなく、パラ言語情報や非音声情報も理解し、さまざまな会話シナリオに合わせた表現豊かな音声応答を生成することが可能になりました。Retrieval-Augmented Generation (RAG)とウェブ検索や音声検索などの外部ツールを活用することで、リアルワールドの知識に基づいた信頼性の高い応答と表現の多様性を提供します。800万時間におよぶ音声データで訓練され、様々なベンチマークで最先端の性能を達成しました。

## 本研究の新規性や貢献
大規模言語モデル（LLM）と音声処理技術の急速な発展により、大規模音声言語モデル（LALM）は従来の音声処理アプローチよりも優位性を示していますが、自然で知的な音声対話の実現には依然として課題が残されていました。先行研究のLALM、例えばSpirit LMやGLM-4-Voiceは、主に「音声入力におけるセマンティック情報のテキストへのアライメント」に注力し、「意図理解に不可欠なパラ言語情報」（paralinguistic information）を軽視していました。Qwen-AudioやAudio Flamingoシリーズはこれらの情報を理解できるものの、「通常テキスト出力のみを生成し、この能力を音声会話で一貫性のある表現豊かな応答を生成するために活用できていませんでした」。さらに、「既存のLALMは、マルチモーダルモデリングの複雑さゆえに、頻繁に幻覚に悩まされ」、また「音色や話し方の選択肢が限られており、実世界のテキストおよび音響知識へのアクセスが不足」していました。

本研究は、これらの課題に対処するため、産業レベルの音声認識と音声対話に特化したエンドツーエンドLALMである「Step-Audio 2」を提案します。その新規性と貢献は、以下の点に集約されます。第一に、潜在音声エンコーダと「推論中心の強化学習」（reasoning-centric reinforcement learning, RL）を統合することで、意味情報だけでなく、パラ言語情報や非音声情報も理解し、表現豊かな音声応答を生成する能力を向上させました。第二に、「離散音声トークンの生成を言語モデリングに組み込む」ことで、真のエンドツーエンドの音声対話を実現し、話し方や感情などのパラ言語情報への応答性を大幅に高めました。第三に、Retrieval-Augmented Generation (RAG)を統合し、ウェブ検索や、「LALMに固有のツールである音声検索」（audio search as a tool unique to LALMs）などの外部ツールを呼び出す能力を持たせることで、幻覚を軽減し、声の指示によるシームレスな音声検索と音色の切り替えを可能にしました。

## 手法
Step-Audio 2は、「音声エンコーダ、音声アダプタ、LLMデコーダ、音声デトクナイザ」から構成されるエンドツーエンドのマルチモーダル大規模言語モデルです。入力された生音声は、まず「様々な音声・音響理解タスクで事前学習され、訓練プロセス中は固定される」（frozen during the entire training process）音声エンコーダによって潜在音声特徴に変換されます。次に、この特徴は音声アダプタによってダウンサンプリングされ、LLMデコーダに供給されます。

LLMデコーダは、音声アダプタから受け取った潜在音声特徴を入力として直接受け取り、離散的なテキストトークンと音声トークンを「インターリーブされたシーケンスとして出力」（outputs an interleaved sequence of discrete text and audio tokens）します。音声トークンは「CosyVoice 2から採用された音声トークナイザ」（tokenizer from CosyVoice 2 [19] as the audio tokenizer）によって生成されます。出力された音声トークンは、音声デトクナイザによって波形に変換されます。音声デトクナイザは、「Flow MatchingモジュールとHiFi-GAN [42] ボコーダ」で構成され、Flow Matchingモジュールが音声トークンからメルスペクトログラムを生成し、ボコーダがそれを波形に変換します。

Step-Audio 2は、リアルワールドの知識を活用し、インタラクティブな機能を拡張するために、様々な外部ツールを統合しています。これには、「音声検索ツール」（audio search tool）、「現在の日付と時刻」、「天気予報」、「ウェブコンテンツ検索」などが含まれます。特に音声検索ツールは、「声の指示によるシームレスな音声検索を可能にし、モデルが検索された音声に基づいて音色や話し方を切り替えることを可能」にします。推論時には、これらの検索された情報が入力音声特徴の後に付加され、音声出力生成に利用されます。

モデルの学習には、綿密に設計された多段階訓練戦略が採用されました。まず、アダプタの音声とテキストの特徴空間の効果的なアライメントのため、100億トークンのASRデータでアダプタを事前訓練します。次に、既存のテキストLLMのトークナイザを6.6Kの音声トークンで拡張し、128億トークンのテキストデータと128億トークンの音声データで訓練します。その後、さらに800億トークンのテキストおよび音声データで主要な事前訓練を実施し、最終的に200億トークンの高品質なテキストおよび音声データで広範なタスクを導入しクールダウンを行います。この包括的な事前訓練により、Step-Audio 2はテキスト性能を維持しつつ、強力な音声理解・生成能力を獲得しました。

さらに、モデルが人間の意図に従い、主要なタスクを習得できるように、「大規模なマルチタスク教師ありファインチューニング」（large-scale, multi-task supervised fine-tuning, SFT）を実施しました。これにより、ASR、音声イベント分類、音声キャプション、パラ言語情報理解、テキスト読み上げ（TTS）、音声間翻訳（S2ST）、テキスト間会話、外部ツール呼び出しなどの多様なタスクをカバーするよう訓練されます。また、複雑な音響シナリオでの音声理解を可能にする「推論中心のデータセット」（reasoning-centric datasets）も構築され、その後の強化学習プロセスをコールドスタートするために利用されました。

音声理解と音声対話におけるモデルの推論能力を向上させるため、マルチステージの強化学習戦略が実装されました。SFTで構築された推論中心のデータセットを活用し、「Proximal Policy Optimization (PPO)」を2段階で適用して推論効率を最適化します。第一段階では、二値報酬関数を用いて思考シーケンス長を制限し、第二段階では、学習済みの報酬モデルを用いて応答品質を評価します。最後に、「group relative policy optimization (GRPO)」を適用し、モデルの音声知覚能力をさらに向上させます。

## 評価方法と結果
Step-Audio 2の性能は、自動音声認識（ASR）、パラ言語情報理解、音声理解、音声翻訳、ツール呼び出し、音声会話の6つの主要なタスクで評価されました。

**ASR**: モデルのASR能力は、英語、中国語の複数のテストセット、日本語、広東語、アラビア語を含む3つの多言語テストセット、および6つの社内中国語方言・アクセント付き標準中国語テストセットで評価されました。Word Error Rate (WER)およびCharacter Error Rate (CER)を用いて、Doubao LLM ASR、GPT-4o Transcribe、Kimi-Audio、Qwen2.5-Omniといった既存のオープンソースおよび商用モデルと比較されました。結果は、「Step-Audio 2は、既存のオープンソースおよび商用ASRモデルを上回り、英語のテストセットで平均WER 3.18%、中国語のテストセットで平均CER 3.11%を達成しました」。多言語および方言においても競争力のある結果を示し、音声の意味理解における優位性が強調されています。

**パラ言語情報理解**: Step-Audio 2が音声中のパラ言語情報をどの程度理解できるか評価するため、独自に「Step-Audio Paralinguistic」というベンチマークが導入されました。これは、11の側面（性別、年齢、音色、感情、ピッチ、リズム、話速、話し方、ボーカル活動、音響イベント、シナリオなど）にわたる単一ターン質問応答形式の音声対音声ベンチマークです。GPT-4o Audio、Kimi-Audio、Qwen-Omni、Step-Audio-AQAAと比較され、「Step-Audio 2は平均精度76.55を達成し、他のベースラインモデルと比較して大幅な改善」を示しました。

**音声理解**: モデルの一般的な音声理解能力は、MMAU-v05.15.25ベンチマークを用いて、音響、音声、音楽の各領域で評価されました。Audio Flamingo 3、Gemini 2.5 Pro、GPT-4o Audio、Kimi-Audio、Omni-R1、Qwen2.5-Omni、Step-Audio-AQAAといったベースラインモデルと比べ、「Step-Audio 2は77.4%という最高の平均スコアを達成」し、特に音響および音楽トラックで最良の結果、音声トラックで最良と並ぶ結果を示しました。

**音声翻訳**: モデルの双方向中国語-英語音声翻訳能力は、CoV oST 2（音声-テキスト翻訳、S2TT）とCVSS（音声-音声翻訳、S2ST）の2つのベンチマークで評価されました。BLEUスコアを評価指標とし、GPT-4o Audio、Qwen2.5-Omni、Qwen-Omni、Step-Audio-AQAAと比較されました。「Step-Audio 2は、中国語-英語双方向翻訳で優れた性能を発揮し、CoVoST 2とCVSSの両テストセットで最高の平均スコアを獲得」しました。

**ツール呼び出し**: 音声会話におけるツール呼び出しのテストセットの不足に対処するため、本研究は「Step-Audio Toolcall」という独自テストセットを導入しました。これは、中国語の音声会話におけるツール呼び出し、選択、パラメータ抽出能力を評価するものです。比較対象として、Qwen3-32B（テキスト入力）が用いられました。「Step-Audio 2は、音声入力であってもテキストLLMと同等のツール呼び出し精度を達成」し、特に「革新的な音声検索ツールの正確な呼び出しにおいてQwen3-32Bを大幅に上回る」結果を示しました。

**音声会話**: 最後に、Step-Audio 2および他のLALM（GPT-4o Audio、Kimi-Audio、Qwen-Omni、Step-Audio-AQAA）は、URO-Benchを用いて評価されました。このベンチマークは、理解、推論、口頭会話能力を評価するものです。「Step-Audio 2は、中国語の音声対音声会話シナリオにおいて、GPT-4o Audioを含む既存のLALMを大幅に上回り、基本トラックで平均スコア78.86、プロトラックで70.83という最高のスコアを達成」しました。英語の音声対音声会話では、「GPT-4o Audioにわずかに劣るものの、非常に競争力のある結果を示し、他のアプローチを上回る」性能を発揮しました。

これらの評価結果から、「Step-Audio 2は、ASR、音声理解、音声翻訳、一般的な音声会話といった多様なタスクにおいて、オープンソースおよび商用ソリューションの両方を上回る最先端の性能を発揮する」ことが示されています。

## 制限事項と課題
本研究の論文「Step-Audio 2 Technical Report」には、Step-Audio 2モデル自体の明確な制限事項や未解決の課題について、明示的なセクションや記述は見当たりません。論文は主に、Step-Audio 2が既存の大規模音声言語モデル（LALM）の課題（パラ言語情報の無視、幻覚、音色の多様性不足など）をいかに克服し、多岐にわたるタスクで最先端の性能を達成したかに焦点を当てています。

ただし、評価結果の「4.6 Speech-to-speech conversation」セクションにおいて、英語の音声対音声会話に関する言及があります。そこでは、「英語の音声対音声会話では、Step-Audio 2はGPT-4o Audioにわずかに劣るものの、非常に競争力のある結果を示し、他のアプローチを上回ります」("In English speech-to-speech conversations, while Step-Audio 2 is slightly outperformed by GPT-4o Audio, it provides very competitive results and exceeds the other approaches.") と述べられています。この「わずかな劣後」は、今後の英語音声会話におけるさらなる性能向上が課題となり得ると解釈できます。

論文の結論部でも、Step-Audio 2の優位性と達成された最先端の性能が強調されており、今後の具体的な研究課題や限界についての記述は含まれていません。したがって、現時点では、英語の音声対音声会話におけるわずかな改善の余地を除き、論文中で明示的に言及されているStep-Audio 2の制限事項や課題は確認できません。

---

*このファイルは自動生成されました。生成日時: 2025年07月23日 08:34:58*
