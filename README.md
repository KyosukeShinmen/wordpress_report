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