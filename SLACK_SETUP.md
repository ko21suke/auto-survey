# Slack通知の設定方法

## 1. Slack Webhook URLの取得

1. Slackワークスペースにログイン
2. [Slack App Directory](https://api.slack.com/apps) にアクセス
3. "Create New App" → "From scratch" を選択
4. アプリ名とワークスペースを選択
5. "Incoming Webhooks" を有効化
6. "Add New Webhook to Workspace" をクリック
7. 投稿先のチャンネルを選択
8. 生成されたWebhook URLをコピー

## 2. 環境変数の設定

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

または、`.env` ファイルを作成：

```bash
echo 'SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"' > .env
```

## 3. 実行

```bash
python main.py
```

## 通知内容

各論文について以下の情報がSlackに送信されます：

- 📄 論文タイトルと著者
- 🎯 研究の目的（要約から抽出、約80文字）
- 🏷️ カテゴリとarXiv ID
- 📖 PDFリンク
- 💾 詳細な要約ファイルの保存場所
- 200字程度の要約

## トラブルシューティング

- `警告: 環境変数 SLACK_WEBHOOK_URL が設定されていません` が表示される場合
  - 環境変数が正しく設定されているか確認してください
  - シェルを再起動するか、`source ~/.bashrc` を実行してください

- Slack通知が失敗する場合
  - Webhook URLが正しいか確認してください
  - ワークスペースの権限を確認してください
  - ネットワーク接続を確認してください