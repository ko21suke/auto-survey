# Auto Survey - 自動技術調査ツール

最新の学術論文を自動的に収集し、AI（Gemini API）を使って要約を生成するツールです。arXivとHugging Face Daily Papersから論文を取得し、Slack通知にも対応しています。

## 機能

- arXivの複数カテゴリから最新論文を自動取得
- Hugging Face Daily Papersからの論文取得
- Gemini APIを使った論文の自動要約
- 重複チェック機能（同じ論文を再処理しない）
- Slack通知（オプション）
- 古い要約ファイルの自動削除
- GitHub Actionsによる定期実行対応

## セットアップ

### 1. 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

以下の環境変数を設定する必要があります：

#### GEMINI_API_KEY（必須）
Google AI StudioでGemini APIキーを取得してください。

```bash
# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"
```

#### SLACK_WEBHOOK_URL（オプション）
Slack通知を使用する場合は、Slack Webhook URLを設定してください。

```bash
# Linux/Mac
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Windows (Command Prompt)
set SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Windows (PowerShell)
$env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 3. GitHub Actionsでの設定（自動実行用）

リポジトリのSettings → Secrets and variablesで以下のシークレットを設定：
- `GEMINI_API_KEY`
- `SLACK_WEBHOOK_URL`（オプション）

## 使い方

### main.pyの基本的な使用方法

```bash
# ツールディレクトリに移動
cd tools

# Hugging Face Daily Papersから論文を取得（デフォルト）
python main.py

# arXivから論文を取得
python main.py -s a

# カスタム設定ファイルを使用
python main.py -c config/custom.yaml
```

### コマンドラインオプション

- `-s, --source`: 論文の取得元を指定
  - `h`: Hugging Face Daily Papers（デフォルト）
  - `a`: arXiv
- `-c, --config`: 設定ファイルのパス（デフォルト: `config/base.yaml`）

## ファイル構成

### 要約ファイルの保存場所

生成された論文要約は `summary/` ディレクトリに保存されます：

```
auto-survey/
├── summary/                    # 要約ファイルの保存場所
│   ├── paper_title_1.md       # 個別の論文要約（Markdown形式）
│   ├── paper_title_2.md
│   └── ...
├── summarized_papers.csv      # 処理済み論文の記録
└── tools/
    └── main.py               # メインスクリプト
```

### 要約ファイルの自動削除

- デフォルトで**7日経過**した要約ファイルは自動的に削除されます
- 削除タイミング：スクリプト実行時の最後
- 削除対象：`summarized_at`から7日以上経過したファイル
- 削除と同時に`summarized_papers.csv`からも該当エントリが削除されます

## 設定ファイル（config/base.yaml）

```yaml
# ArXiv configuration
arxiv:
  categories:
    - cs.RO    # Robotics
    - cs.CV    # Computer Vision
    - cs.LG    # Machine Learning
    - cs.AI    # Artificial Intelligence
    - cs.SY    # Systems and Control
  max_papers_per_category: 3    # 各カテゴリから取得する最大論文数

# Hugging Face configuration
hugging_face:
  max_papers: 1    # 取得する最大論文数
```

### 設定項目の説明

- **arxiv.categories**: 監視対象のarXivカテゴリ
- **arxiv.max_papers_per_category**: 各カテゴリから取得する論文数の上限
- **hugging_face.max_papers**: Hugging Face Daily Papersから取得する論文数の上限

## GitHub Actionsによる自動実行

`.github/workflows/auto-survey.yml`により、以下のスケジュールで自動実行されます：

- **実行時間**: 平日17時（日本時間）
- **手動実行**: GitHub ActionsのUIから手動実行も可能

## 生成される要約の内容

各論文の要約には以下が含まれます：

1. **基本情報**
2. **研究の概要？**
3. **本研究の新規性や貢献**
4. **研究の手法**
5. **評価方法と結果**
5. **制限事項と課題**

## トラブルシューティング

### エラー: GEMINI_API_KEY が設定されていません
→ 環境変数 `GEMINI_API_KEY` を設定してください

### 警告: SLACK_WEBHOOK_URL が設定されていません
→ Slack通知が不要な場合は無視して構いません

### 論文が取得できない
→ ネットワーク接続を確認し、arXivやHugging Faceのサービス状態を確認してください

