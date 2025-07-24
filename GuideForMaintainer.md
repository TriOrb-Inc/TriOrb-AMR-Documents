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

## Tips
### Gemfileの作り方
#### rbenv と ruby-buildのインストール
```bash
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
echo 'export PATH="~/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
source ~/.bashrc
rbenv -v
 
git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build
sudo apt install -y build-essential libssl-dev zlib1g-dev
rbenv install --list
rbenv install 3.1.2
rbenv global 3.1.2
ruby -v
```
### Ruby のバージョン指定
```bash
echo "3.1.2" > .ruby-version
```
#### Gemfileの新規作成
```bash
bundle init
# これでGemfileが生成される
```
#### Gemfileの編集
```bash
# nano ./Gemfile
source "https://rubygems.org"
gem "jekyll", "~> 4.3.2"
```
#### Gemfileのインストール
```bash
bundle install
# これでGemfile.lockが生成される
```