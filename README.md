# TriOrb-AMR-Documents（本リポジトリ編集者へのガイド）
このドキュメントは、API公開Webサイトの生成と更新に関するガイドです。
公開ページのHomeは`triorb-amr-docs/docs/index.md`にあります。

## TriOrb開発者がメンテナンスすべきファイル
- `triorb-amr-docs/docs/index.md`: 公開サイトのトップページ
- `submodules/TriOrb-AMR-Package/pkgs/folder_descriptions.json`: 各フォルダの説明文
- `submodules/TriOrb-AMR-Package/pkgs-collab/folder_descriptions.json`: 各フォルダの説明文（協調移動パッケージ群）
- `submodules/TriOrb-AMR-Package/**/package.xml`: 各パッケージのメタ情報のうち`<description>`タグ

## リポジトリ環境初期構築
```bash
git clone git@github.com:TriOrb-Inc/TriOrb-AMR-Documents.git
cd TriOrb-AMR-Documents
git submodule update --init --recursive
```
## submoduleのバージョンをアップデート
```bash
bash -c 'cd submodules/triorb-core && git checkout master && git pull && git submodule update --init --recursive'
bash -c 'cd submodules/TriOrb-AMR-Package && git checkout master && git pull && git submodule update --init --recursive'
```
## 自律移動パッケージのAPIリファレンス生成
```bash
bash -c 'cd submodules/TriOrb-AMR-Package && sh dev/generate_document.sh ${VERSION} ${DATE}'
```

## 最新パッケージから*.mdと*.ipynbを収集
```bash
python3 gather_md.py
# README.mdをルートとして生成されたページツリーの内容が適切かどうか目視確認する
```

### Markdownからビルド
```bash
source .venv/bin/activate
pip install -r mkdocs_requirements.txt
cd triorb-amr-docs
mkdocs build
```

### バージョン付きデプロイ（mike）
```bash
source .venv/bin/activate
pip install -r mkdocs_requirements.txt
cd triorb-amr-docs
mike deploy v1.2.3 # 手元でビルドするだけ
mike deploy --push --branch gh-pages v1.2.3 # 単に個別バージョンをデプロイ
mike deploy --push --branch gh-pages --update-aliases v1.2.3 latest # latestに紐づけてデプロイ
mike set-default --push --branch gh-pages latest

# 公開済みバージョンを確認
mike list
```

`mike deploy` 時に `--title` オプションを指定すると、バージョン切り替えメニューに表示する名称を任意に設定できます。

> `--branch` にはデプロイ先を指定します（GitHub Pages を利用する場合は通常 `gh-pages`）。初回のみ `mike set-default` で既定バージョンを設定してください。
```

## Tips
### MkDocs環境セットアップ
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install mkdocs mkdocs-material mkdocs-material-extensions
python3 -m pip freeze > mkdocs_requirements.txt
```
### MkDocsプロジェクト作成
```bash
source .venv/bin/activate
mkdocs new triorb-amr-docs
```
### MkDocs開発サーバー起動
```bash
source .venv/bin/activate
cd triorb-amr-docs
#mkdocs serve -a 0.0.0.0:18000
mike serve -a 0.0.0.0:18000
# ブラウザで http://${HOST_IP}:18000 を開く
```
