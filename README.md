# 🐦 RSS to X (Twitter) Poster

指定したRSSフィードからランダムに1件の記事を取得し、X（旧Twitter）へ自動投稿するPythonスクリプトです。

## 🔧 主な機能

- RSSから記事タイトルとURLを取得
- 任意の接頭辞（ステータス）とハッシュタグを付与してXに投稿
- `.env`またはGitHub Actionsの`secrets`で柔軟に設定
- `TEST_MODE`で投稿をせず出力のみも可能

## 🚀 使用方法

### 1. 依存パッケージをインストール

`pip install -r requirements.txt`

### 2. .env ファイルを作成（または環境変数に設定）

`X_API_KEY=xxxxx`

`X_API_SECRET=xxxxx`

`X_ACCESS_TOKEN=xxxxx`

`X_ACCESS_SECRET=xxxxx`



`FEED_URL=https://www.example.com/feed/`

`HASHTAGS=#ブログ #自動投稿`

`STATUS_PREFIX=【注目記事】`

`TEST_MODE=true  # trueにすると投稿せずログ出力のみ`

※ .env を使うには python-dotenv を導入してください（このスクリプトでは未使用です）。

-------

### 3. スクリプトを実行

| 変数名               | 必須 | 説明                                |
| ----------------- | -- | --------------------------------- |
| `X_API_KEY`       | ✅  | X API (Twitter API) のConsumer Key |
| `X_API_SECRET`    | ✅  | Consumer Secret                   |
| `X_ACCESS_TOKEN`  | ✅  | Access Token                      |
| `X_ACCESS_SECRET` | ✅  | Access Token Secret               |
| `FEED_URL`        | ✅  | RSSフィードのURL                       |
| `HASHTAGS`        | 任意 | 投稿時に末尾に追加されるハッシュタグ（複数可）           |
| `STATUS_PREFIX`   | 任意 | 投稿文の冒頭に追加されるプレフィックス例: `【アーカイブ】`など |
| `TEST_MODE`       | 任意 | `true`にすると投稿せずログのみ出力              |



## ❗ 注意事項


X APIのアクセスレベル制限 により、EssentialプランではPOST /2/tweetsが使用できないことがあります。

エラーが出る場合は Elevated または Academic Research への申請が必要です。

詳細: https://developer.x.com/en/portal/product


## 📄 ライセンス


改変・拡張する場合は以下URLから一報ください。 （基本的にはNGを出しません。共有OKであれば本サイトで紹介します。）

URL：https://www.cybernote.click/contact/

（題名に「AWS Status Notifier改変・拡張の件」と記載して、メッセージ本文に改変内容を明記してください）
