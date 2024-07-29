# CUIコマンドのwebAPI化**ドキュメント**

# 環境設定
## 開発環境
    OS: Ubuntu 20.04.6 LTS
    python: 3.8.10
## インストール
- pipのインストール
    $ sudo apt update
    $ sudo apt install python3-pip


- fast apiのインストール
    - 参考：[https://fastapi.tiangolo.com/ja/tutorial/](https://fastapi.tiangolo.com/ja/tutorial/#fastapi)
    - すべての依存関係をインストール（サーバー`uvicorn` もインストールされる）
    $ pip install fastapi[all]
    - 個別にインストールしたい場合
    $ pip install fastapi
    $ pip install "uvicorn[standard]"


- 下記のプログラムを設置（例えばホームにapiディレクトリをつくる）
    - ファイル構成
        - api/main.py
            - CUIコマンドのAPI化
        - api/sample.html
            - サンプルHTM
    - その他
        - boot.sh
            - 自動起動スクリプトファイル
        - cui_execute.service
            - 自動起動サービス
        - html設計書
- 自動起動の設定
    - /etc/systemd/system/にcui_execute.serviceを移動
        - 適宜、boot.sh, cui_execute.serviceのファイルパスを変更
    - サービスのstart
    systemctl start cui_execute.service
    - サービスの停止
    systemctl stop cui_execute.service
    - サービスの自動起動
    systemctl enable cui_execute.service
    - 
# テスト
- APIサーバーの起動
    cd /home/user/api/
    python3 -m uvicorn main:app --reload
    - 開発時に--reloadオプションを追加しておくとプログラム修正時に自動でリロードされる
    - 実運用時は以下
    python3 -m uvicorn main:app --host=0.0.0.0 --port=3000
- サンプルHTML（sample.html）を任意のブラウザで開く


# 設計書
## APIドキュメント
- doc/api_doc.pdf
- 以下にアクセスしてもOK
    - htpp://localost:8000/docs
    - 自動生成されたAPIドキュメントが見れる
## 画面設計書
- doc/html設計書.xlsx

