# TriOrb-AMR-Documents（本リポジトリ編集者へのガイド）
このドキュメントは、API公開Webサイトの生成と更新に関するガイドです。
公開ページのHomeは`triorb-amr-docs/docs/index.md`にあります。

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
bash -c 'cd submodules/TriOrb-AMR-Package && sh dev/generate_document.sh'
```

## 最新パッケージから*.mdと*.ipynbを収集
```bash
python3 gather_md.py
# README.mdをルートとして生成されたページツリーの内容が適切かどうか目視確認する
```

### Markdownからビルド
```bash
source .venv/bin/activate
cd triorb-amr-docs
mkdocs build
```

### GitHub Pagesにデプロイ
```bash
source .venv/bin/activate
cd triorb-amr-docs
mkdocs gh-deploy
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
mkdocs serve -a 0.0.0.0:18000
# ブラウザで http://${HOST_IP}:18000 を開く
```