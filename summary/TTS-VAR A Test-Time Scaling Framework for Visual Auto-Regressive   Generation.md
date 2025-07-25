# TTS-VAR: A Test-Time Scaling Framework for Visual Auto-Regressive   Generation

**arXiv ID**: [2507.18537](http://arxiv.org/abs/2507.18537v1)
**PDF**: [ダウンロード](http://arxiv.org/pdf/2507.18537v1.pdf)
**著者**: Zhekai Chen, Ruihang Chu, Yukang Chen, Shiwei Zhang, Yujie Wei, Yingya Zhang, Xihui Liu
**カテゴリ**: cs.CV
**公開日**: 2025-07-24T16:04:55Z

---

## 要約

## #0ショートサマリ
本研究は、ビジュアル自己回帰（VAR）モデルにおける画像生成のスケーリングが、多大なトレーニングと計算コストを必要とする課題を解決します。既存のテスト時スケーリング手法では、VARの効率を損ねたり、初期段階の評価が不正確であるという問題がありました。本研究は、初の汎用VARモデル向けテスト時スケーリングフレームワーク「TTS-VAR」を提案します。これは、生成プロセスをパス探索問題と捉え、計算効率と探索能力を動的にバランスさせるため、適応的なバッチサイズスケジュールを導入。さらに、粗いスケールでの「クラスタリングベースの多様性探索」と、細かいスケールでの「リサンプリングベースのポテンシャル選択」を統合しました。強力なVARモデルInfinityでの実験により、GenEvalスコアを0.69から0.75に8.7%向上させる notable な結果を示しました。

## #1本研究の概要
ビジュアル生成モデルのスケーリングは、リアルワールドでのコンテンツ制作に不可欠ですが、多大なトレーニングと計算コストを必要とします。リソース効率と有望なパフォーマンスから、テスト時スケーリングが注目されています。本研究の目的は、ビジュアル自己回帰（VAR）モデルにテスト時スケーリングを適用し、その性能を向上させることです。VARモデルは、画像を多スケールの粗密表現にエンコードし、階層的な集約を通じて画像を段階的に合成する画期的なパラダイムです。

本研究では、VARモデル向けの初の汎用テスト時スケーリングフレームワーク「TTS-VAR」を提案し、この目的を達成しました。TTS-VARは、生成プロセスをパス探索問題としてモデル化し、計算効率と探索能力を動的にバランスさせるために適応的なバッチサイズスケジュールを導入。さらに、VARの階層的な粗密生成にインスパイアされ、粗いスケールでの「クラスタリングベースの多様性探索」と、細かいスケールでの「リサンプリングベースのポテンシャル選択」という2つの主要コンポーネントを統合しました。実験では、強力なVARモデルInfinityにおいて、GenEvalスコアを notable な8.7%向上させることに成功しました。

## #2本研究の新規性や貢献
画像生成モデルのスケーリングは重要ですが、莫大な訓練コストが課題です。このため、テスト時スケーリングが注目を集めています。しかし、自己回帰（AR）モデルにおける既存のテスト時スケーリング手法には限界がありました。例えば、一部の先行研究では追加学習が必要であったり、生成プロセス自体を見落としていたりしました。拡散モデルにおけるパス探索戦略も、VARモデルに直接適用するのは困難でした。VARモデルでは、生成されたトークンは固定され、各トークンが後続のトークン生成に直接影響を与えるため、初期段階の品質の低いトークンに対する許容度が低く、初期段階での評価が不正確であるという課題がありました。

本研究は、これらの課題に対応し、VARモデルに特化した初の汎用テスト時スケーリングフレームワーク「TTS-VAR」を提案しました。これは、VARの因果的な粗密生成プロセスに合わせたスケーリング戦略を統合することで、既存手法の限界を克服します。具体的には、初期スケールで評価が困難な状況での多様性保持と、後期スケールでの正確な評価に基づく候補選択という二段階のアプローチにより、従来のDiffusionモデルベースのパス探索やARモデルにおけるCoT（Chain-of-Thought）アプローチの限界を解決し、大幅な性能向上を達成した点に新規性があります。

## #3手法
本研究のTTS-VARは、画像生成プロセスをパス探索問題として捉え、計算効率と探索能力を動的にバランスさせることを目指します。

まず、VARモデルの特性として、シーケンス長が長くなるにつれてRAMメモリ消費と計算コストが増加することに着目し、「adaptive descending batch size schedule」を導入します。これにより、初期スケールではより多くのサンプルを生成し、後期スケールではサンプル数を減らすことで、全体の計算消費を抑えつつ、より多くの可能性を探索します。例えば、「For a typical VAR model encompassing 13 scales, the batch size schedule is { 8N, 8N, 6N, 6N, 6N, 4N, 2N, 2N, 2N, 1N, 1N, 1N, 1N} unless otherwise specified.」と設定されます。

次に、VARの階層的粗密生成プロセスに合わせて2つの主要コンポーネントを統合します。
1. **クラスタリングベースの多様性探索（Clustering-Based Diversity Search）**: 粗いスケールでは、生成されたトークンが評価しにくく、最終結果の品質と乖離する可能性があるため、多様性を維持することを目指します。早期のスケールから構造情報が伝達されるという観察に基づき、DINOv2のような「semantic features extracted by pre-trained extractors like DINOv2」を用いて、中間画像を意味的特徴空間に埋め込みます。その後、K-Means++アルゴリズムを適用してクラスタリングし、「select samples with the shortest L2 distance to cluster centers as new batches」とすることで、構造的な多様性を保持し、後の選択に備えます。
2. **リサンプリングベースのポテンシャル選択（Resampling-Based Potential Selection）**: 細かいスケールでは、中間画像が最終結果と高い整合性を示すため、報酬関数が直接生成をガイドできます。ここでは、多スケール生成履歴を組み込んだ「potential scores, which are defined as reward functions incorporating multi-scale generation history」を用いて、有望な候補を優先的にリサンプリングします。様々なポテンシャルスコア（VALUE, DIFF, MAX, SUM）を検討した結果、「VALUE performs well」とされており、ImageRewardを報酬関数として利用します。

## #4評価方法と結果
本研究は、提案手法TTS-VARの有効性を、強力なVARモデルであるInfinity-2B上で検証しました。評価にはImageReward [53] を報酬関数として用い、GenEval [54] とT2I-CompBench [55] を主要な指標としました。さらに、ImageReward [53]、HPSv2.1 [56,57]、Aesthetic V2.5 [58]、CLIP-Score [59,60] といった関連指標も分析に含めました。評価はGenEvalが提供するプロンプトに基づいて実施されました。

結果として、TTS-VARは既存のSOTAモデルや従来のテスト時スケーリング戦略（Importance SamplingやBest-of-N）を大幅に上回る性能を示しました。「TTS-VAR achieves an overall GenEval score of 0.7530 at N= 8, surpassing the record 0.74 of Stable Diffusion 3 (8B parameters) while utilizing 60% fewer parameters.」また、「even with minimal computational overhead ( N= 2), our approach attains the competitive performance of score 0.7403, outperforming Best-of-N ( N= 8) with only 25% sample number.」T2I-CompBenchでも、ベースモデルと比較して全ての指標で顕著な改善が見られ、N=2でBest-of-N (N=8)を上回る結果を達成しました。

実験結果の分析から、「resampling at early scales (e.g., scale 3) leads to a noticeable decline in the final results. Instead, resampling at later scales yields a certain degree of improvement.」という洞察が得られました。これは、初期スケールでは中間状態の評価スコアが最終画像と低い整合性を示し、スケール6以降で高い整合性を示すため、「scores become valuable from a certain late scale, like scale 6, with comparatively high consistency. This explains why resampling efficacy varies and should be applied selectively on later scales.」と考察されています。ポテンシャルスコアに関しては、「VALUE and MAX achieve the highest scores in text-related metrics such as GenEval, ImageReward, and HPS」ことを確認しました。クラスタリングベースの多様性探索については、スケール2と5での適用が特に効果的であり、「each clustering increases the likelihood of yielding better results, and there is an obvious growth when employing both scales.」また、DINOv2のPCA変換された特徴が最良の結果をもたらすことが示されました。特に、「2つのオブジェクト」や「カウント」のタスクで顕著な改善が見られ、「TTS-VAR facilitates structure diversity, thereby enabling the selection of a layout with the correct configuration and avoiding the irreversible wrong generation process for inferior samples.」と述べられています。

## #5制限事項と課題
本研究のTTS-VARは、ベースラインに対して顕著な改善を示し、新しい記録を打ち立てましたが、主に2つの制限事項と今後の課題を抱えています。

第一に、「TTS-VAR does not completely address the misalignment between text prompts and generated images. As indicated by the scores in Table 7, there are still some failure cases, particularly in the Position item.」これは、テキストプロンプトと生成された画像の不一致を完全に解決できていないことを示しており、特に位置関係の指定において課題が残っています。

第二に、「while TTS-VAR is based on a general coarse-to-fine process, its potential application to other coarse-to-fine models, such as autoregressive models that use 1-D tokenizers, remains unexplored.」本研究のフレームワークは一般的な粗密生成プロセスに基づいているものの、1次元のトークナイザーを使用する自己回帰モデルなど、他の粗密モデルへの適用可能性については未探索です。

今後の研究課題としては、「we will investigate the generation process more thoroughly, examining the reasons for failure and designing solutions to unlock further scaling potential.」と述べており、失敗の根本原因をさらに深く調査し、さらなるスケーリングの可能性を引き出すための解決策を設計することを目指しています。加えて、「Additionally, we plan to assess the compatibility of TTS-VAR with other autoregressive coarse-to-fine models, including those utilizing 1-D tokenizers and hybrid architectures that combine diffusion models.」と述べ、他の自己回帰粗密モデルや、拡散モデルを組み合わせたハイブリッドアーキテクチャとの互換性を評価する計画です。これにより、テキストから画像への合成のためのより堅牢なスケーリングフレームワークを構築し、粗密パラダイムの汎用性を高めることを目指しています。また、本手法の誤用によるプライバシーや著作権に関する懸念といった「potential societal impact on privacy and copyright」も認識しています。

---

*このファイルは自動生成されました。生成日時: 2025年07月25日 08:33:42*
