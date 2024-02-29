# TriOrb-AMR-Package
TriOrb AMRのための自律移動パッケージ配布用Root。このリポジトリには、Host(Jetson OS)で直接実行するROSパッケージ群と、Dockerコンテナで実行するROSパッケージ群が含まれている。
- ./host_pkgs : Hostで直接実行するROSパッケージ群
- ./vm_pkgs : Dockerコンテナで実行するROSパッケージ群

## [Hostで直接実行するROSパッケージ群マニュアル](./host_pkgs/README.md)
なお、上記README記載のコマンドは原則カレントディレクトリを```cd ./host_pkgs```と移動した状態を前提としている。

## [Dockerコンテナで実行するROSパッケージ群マニュアル](./vm_pkgs/README.md)
なお、上記README記載のコマンドは原則カレントディレクトリを```cd ./vm_pkgs```と移動した状態を前提としている。

# Tips
## submodules update
```bash
git submodule update --init --recursive &&\
git submodule update --recursive --force --checkout --remote
```
