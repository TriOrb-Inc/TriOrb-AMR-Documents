# 本リポジトリ編集者へのガイド
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