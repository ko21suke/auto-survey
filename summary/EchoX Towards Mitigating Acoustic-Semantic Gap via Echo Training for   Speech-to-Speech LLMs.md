# EchoX: Towards Mitigating Acoustic-Semantic Gap via Echo Training for   Speech-to-Speech LLMs

**arXiv ID**: [2509.09174](http://arxiv.org/abs/2509.09174v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2509.09174v1.pdf)
**著者**: Yuhao Zhang, Yuhao Du, Zhanchen Dai, Xiangnan Ma, Kaiqi Kou, Benyou Wang, Haizhou Li
**カテゴリ**: cs.CL, cs.AI, cs.SD
**公開日**: 2025-09-11T06:17:59Z

---

## 要約

## #0ショートサマリ
SLLM（Speech-to-Speech Large Language Models）は、テキストベースLLMに由来するものの、知識や推論能力の劣化が課題でした。本研究は、この問題が「特徴表現空間における音響-意味ギャップ」にあると仮説を立て、その解決を目指しました。提案する「EchoX」は、意味表現を活用して動的に音声訓練ターゲットを生成する「Echo Training」を導入することで、音響学習と意味学習を統合し、音響-意味ギャップを緩和します。さらに、効率的な「単位言語」と「ストリーミング生成」機構を採用しました。実験の結果、EchoXは約6000時間のデータで、複数の知識ベースQ&Aベンチマークにおいて、先行研究のモデル（数百万時間で訓練されたモデルを含む）と同等の優れた性能を達成し、効率的なSLLM構築の可能性を示しました。

## #1本研究の概要
本研究は、SLLM（Speech-to-Speech Large Language Models）がテキストベースのLLM（Large Language Models）と比較して知識や推論能力が劣化するという課題の解決を目的としています。この劣化は、現在のSLLMの訓練パラダイムが「特徴表現空間における音響-意味ギャップ」を解消できていないことに起因すると仮説を立てています。例えば、「Hello」と「Hi」は意味的に近いが音響は異なり、音声LLMの訓練では発音レベルの正確性が重視されるため、意味的に正しい出力でも発音の違いで不当なペナルティを受ける問題が生じていました。

本研究は、この問題を解決するために「EchoX」という新しいフレームワークを提案しました。EchoXは、意味表現を活用して音声訓練ターゲットを動的に生成する「Echo Training」戦略を導入し、音響学習と意味学習を統合します。これにより、EchoXは強力な推論能力を保持するSLLMを構築することに成功しました。実験の結果、約6000時間の訓練データで、複数の知識ベースQ&Aベンチマークにおいて高い性能を達成し、限られたデータ量とパラメータで効率的にSLLMの知能を維持できることを示しました。

## #2本研究の新規性や貢献
SLLM（Speech-to-Speech Large Language Models）分野では、テキストベースLLM（Large Language Models）の知能を音声領域に完全に拡張できておらず、「知能劣化」が主要な課題として認識されています。この問題の根源は、「特徴表現空間における音響-意味ギャップ」にあると本研究は指摘しています。例えば、従来のSLLMでは、意味的に同義の単語であっても、音響的な差異が大きい場合にモデルがペナルティを受けてしまい、発音レベルの正確性に訓練が偏るという問題がありました（Figure 1(b)）。

関連する先行研究には、音響と意味を同時に学習する「interleaved generation」や、テキスト表現を音声トークンに変換する「text-to-codec decoder」がありますが、「interleaved generation」は膨大な訓練データを必要とし、「text-to-codec decoder」は音響-意味ギャップを完全に解決できていませんでした。

本研究は、この既存手法の限界を乗り越えるために、「EchoX」という新しいアプローチを提案します。特に、「Echo Training」という独自の手法を導入することで、意味理解に基づいて音声トークンを動的に生成し、音声トークンと意味特徴のミスマッチを効果的に解消します。これにより、SLLMがLLMの強力な知能を維持できるようになります。約6000時間の限られたデータで、数百万時間で訓練されたモデルに匹敵する性能を達成したことは、効率的かつ高性能なSLLMの実現に向けた重要な貢献です。

## #3手法
本研究では、SLLM（Speech-to-Speech Large Language Models）における音響-意味ギャップを緩和するため、EchoXという三段階の訓練フレームワークを提案します。

第一段階「Speech-to-Text Training (S2T)」では、Soundwaveのような既存技術を活用し、テキストLLMを音声-テキスト対話LLMに変換します。これにより、モデルは音声入力を理解し、テキスト応答を生成できるようになります。
第二段階「Text-to-Codec Training (T2C)」では、テキストを量子化された音声トークンに変換するデコーダーのみのモデルを訓練します。
第三段階「Echo Training」が本手法の中核であり、前二段階で訓練されたモジュールを結合し、SLLM全体をファインチューニングします。この段階では、「conventional approaches that rely on annotated speech tokens for training, we propose Echo training, which leverages the pre-trained T2C module to decode the outputs of the S2T LLM as training targets.」（2.4節）とあるように、S2T LLMからの中間表現Hを、訓練済みのT2Cモジュールに通して音声トークンY'を擬似ラベルとして動的に生成し、これをEchoデコーダーの訓練ターゲットとします。訓練目的は「`L_Echo = sum(log P(y'_i | H, y'_<i))`」（式1）で定義されます。

さらに、中間表現Hの冗長な情報を軽減し、Hとそれに対応するテキストX'の埋め込み表現の整合性を図るため、「we design a feed-forward network, termed the Denoising Adapter, before feeding them into the Echo decoder. The purpose is to align the representations between H and the embeddings of X'.」（2.4節）とあり、Denoising Adapterを導入します。その損失は「`L_Denoising = sum(1 - Cos(Adapter(H_i), Emb(X'_i)))`」（式2）で計算され、最終的な訓練損失は、S2T LLMのLoRAパラメーター更新のためのS2T損失`L_S2T`とこれら二つの損失を重み付け合計した「`L = L_Echo + λ * L_Denoising + L_S2T`」（式4）です。
また、長尺音声シーケンスの課題に対処するため、音声トークンには「unit language（単位言語）」という効率的な表現を使用し、「streaming generation（ストリーミング生成）」機構を導入しています。

## #4評価方法と結果
本研究では、EchoXの性能を、知識ベースの質問応答タスクにおいて評価しました。評価は「Llama questions」、「Web questions」、および「TriviaQA」の3つの主要なベンチマークを用いて行われ、評価ツールとして「UltraEval-Audio」を使用しました。比較のために、3Bと8Bの2種類のモデルサイズで実験を実施しています。

得られた結果の概要として、「EchoX, with about six thousand hours of training data, achieves advanced performance on multiple knowledge-based question-answering benchmarks.」（Abstract）と述べられており、本モデルは約6000時間の訓練データで、複数の知識ベースQ&Aベンチマークにおいて優れた性能を達成しました。特に、Table 2のSpeech-to-Speech性能では、EchoX-3Bが平均37.1、EchoX-8Bが平均46.3を記録し、「EchoX trained with about six thousand hours of data, achieves comparable performance with models trained on millions of hours.」（4.2節）と示されているように、数百万時間ものデータで訓練された先行研究のモデル（例：VITA-Audio、MinMo）に匹敵する性能を示しました。

この結果の解釈として、本研究は「our proposed Echo training strategy offers an efficient way to learn unified speech and semantic representations.」（4.2節）と述べています。これは、提案されたEchoトレーニング戦略が、統一された音声表現と意味表現を効率的に学習するための効果的な手段であることを実証しています。さらに、ストリーミング生成の分析（Table 6）では、このアプローチが性能を大きく劣化させることなく、特にモデル容量が限られた3Bモデルにおいて、長いシーケンス生成の困難さを軽減し、良好な性能に寄与することが示されました。

## #5制限事項と課題
本研究における主な制限事項と今後の課題は、SLLM（Speech-to-Speech Large Language Models）の知能劣化と、それが引き起こす音響-意味ギャップに関連しています。分析セクションでは、「the learning objectives for semantics and acoustics are not aligned, necessitating the design of solutions to address this issue.」（5.2節）と述べられており、意味と音響の学習目的が一致していないことが根本的な課題であると指摘されています。これは、モデルが意味的な正確さよりも発音レベルの正確さに偏ってしまうという問題に繋がります。

また、音声トークンとして「単位言語」を使用しているものの、中間表現からの音声トークン予測において「it is prone to error accumulation, leading to an increased error rate in the final model predictions.」（5.3節）と述べられており、エラーが蓄積し、最終的なモデル予測のエラー率が増加する可能性が示唆されています。

さらに、人間による評価（Figure 8）では、EchoXは質問に対する応答の「helpfulness（有用性）」において強みを見せた一方で、「naturalness is more dependent on the prosodic quality of the generated speech. Since our training focuses on preserving semantic reasoning and efficiency rather than detailed acoustic modeling, EchoX still lags behind stronger speech synthesis models in producing fully human-like intonation.」（Appendix C）と指摘されています。EchoXの訓練は、セマンティックな推論能力の保持と効率性に重点を置いているため、生成される音声の自然さ、特に人間らしいイントネーションの品質では、より強力な音声合成モデルに劣る可能性があります。このため、今後の研究課題として、「future work should further refine speech generation modules to improve naturalness.」（Appendix C）と述べられており、音声生成モジュールをさらに洗練させ、自然さを向上させることが挙げられています。

---

*このファイルは自動生成されました。生成日時: 2025年09月12日 08:28:31*
