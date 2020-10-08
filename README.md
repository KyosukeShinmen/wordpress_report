# 概要
WordPress、Analytics、Search Consoleと連携して以下を記事IDごとにスプレッドシートに書き込むことができます。
デフォルトで書き出せる内容は下記の通り。

- 記事ID
- 記事タイトル
- 記事URL
- サムネイルURL
- PV（Google Analyticsから取得）
- リード文（post_contentのテキストの冒頭300文字）
- 文字数
- 内部リンク一覧（post_content内aタグのhref）
- 記事内画像（post_content内imgタグのsrc）
- 投稿日
- 最終更新日
- Googleの検索順位

# 使い方
- 後述の必要モジュールをインストール
- JSONキーファイルをindex.pyと同階層に設置
- config.iniファイルをindex.pyと同階層に設置
- cmdでindex.pyがあるディレクトリまで移動
- python index.py

# 必要モジュールのインストール
下記をコマンドラインから実行

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install pymysql
pip install bs4
pip install oauth2client
pip install gspread
pip install tqdm
pip install pandas
```

# config.ini
下記のように記述を行う

```config.ini
[GoogleAPI]
key_file = JSONキーファイルのファイル名
analytics_view = アナリティクスのviewID
spreadsheet_name = スプレッドシート名
search_console_url = サーチコンソールで登録しているドメイン、URL

[DB]
host = 接続先のホスト名
user = ユーザー名
password = パスワード
prefix = DBの接頭字（例：{prefix}_posts）
table_name = データベース名

[other]
home = トップページのURL
```