# PostgreSQLをwindowsで使用する手順

1. [PostgreSQLをwindowsにインストール](https://ai-trend.jp/programming/db/postgre-windows-install/)
1. [PostgreSQLのpathを通す](https://www.dbonline.jp/postgresql/install/index3.html)
    1. `\l [SQL shell]` で作成されているデータベースを確認(出力結果は以下＝デフォルト)
    ```
       名前    |  所有者  | エンコーディング |      照合順序      | Ctype(変換演算子)  |     アクセス権限
    -----------+----------+------------------+--------------------+--------------------+-----------------------
     postgres  | postgres | UTF8             | Japanese_Japan.932 | Japanese_Japan.932 |
     template0 | postgres | UTF8             | Japanese_Japan.932 | Japanese_Japan.932 | =c/postgres          +
               |          |                  |                    |                    | postgres=CTc/postgres
     template1 | postgres | UTF8             | Japanese_Japan.932 | Japanese_Japan.932 | =c/postgres          +
               |          |                  |                    |                    | postgres=CTc/postgres
    (3 行)
    ```
1. `CREATE DATABASE warikan; [SQL shell]` warikanというデータベースを作成
1. `CREATE USER warikanmanager WITH PASSWORD '1234'; [SQL shell]` warikanmanagerというユーザー（パスワード＝1234）を作成
1. `pip install psycopg2-binary [python環境]`
1. `python manage.py makemigrations [python環境 manage.pyのある階層]`
1. `python manage.py migrate [python環境 manage.pyのある階層]`
1. `python manage.py createsuperuser [python環境 manage.pyのある階層]`
    1. username ご自由に
    1. email スキップ可能
    1. password ご自由に
1. `python manage.py runserver [python環境 manage.pyのある階層]` (デフォルトで8000ポートで起動するが、そのポートをほかで使っている場合は8888など自分で指定)
    1. localhost:8000/にアクセス(ロケットが飛んでいることを確認)
    1. localhost:8000/adminにアクセス(先程作成したユーザーでログインできることを確認)

<br>

参考:
- [Django PostgreSQL 設定](https://qiita.com/shigechiyo/items/9b5a03ceead6e5ec87ec)