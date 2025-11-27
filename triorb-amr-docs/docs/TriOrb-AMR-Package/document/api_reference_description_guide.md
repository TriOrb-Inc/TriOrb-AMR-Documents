# APIリファレンス用フォルダ説明の更新手順

自律移動API (`pkgs`) と協調移動API (`pkgs-collab`) のジェネレーターは、トップレベルフォルダごとの説明を以下の優先順で読み込み、インデックスページに表示します。

1. `folder_descriptions.json` の定義（トップレベルディレクトリ直下）
2. 各トップレベルフォルダ直下の `DESCRIPTION.md`
3. いずれも無い場合は空欄

## 主に更新するファイル

- `pkgs/folder_descriptions.json` — 自律移動API用のフォルダ説明を定義します。
- `pkgs-collab/folder_descriptions.json` — 協調移動API用のフォルダ説明を定義します。
- `<トップレベルフォルダ>/DESCRIPTION.md` — JSONに書けない詳細説明や長文を置きたい場合にフォルダ直下へ追加します（例: `pkgs/triorb_drive/DESCRIPTION.md`）。
- パッケージ個別の概要は各パッケージの `README.md` または `API.md` を編集してください（ジェネレーターが読み込んでパッケージページを生成します）。

## 反映方法

1. 上記ファイルを更新後、リポジトリルートで `sh dev/generate_document.sh` を実行します。
2. `pkgs/Reference_API/` および `pkgs-collab/Reference_API/` 配下の生成物が更新され、MkDocs/mike 配下に反映されます。

## 補足

- `folder_descriptions.json` はキーにトップレベルフォルダ名、値に説明文を指定します。省略したフォルダは自動的に `DESCRIPTION.md` を参照します。
- `DESCRIPTION.md` はMarkdownの本文がそのままインデックスの説明として表示されます。
- 生成スクリプトは各パッケージの `package.xml` から description 要素も拾うため、簡潔な要約は `package.xml` に残しておくと一覧表示が充実します。
