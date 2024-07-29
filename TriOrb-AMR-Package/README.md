# TriOrb-AMR-Package
TriOrb AMRのための自律移動パッケージ配布用Root。
- ./pkgs : ROSパッケージ群

## [Dockerコンテナで実行するROSパッケージ群マニュアル](./pkgs/README.md)
なお、上記README記載のコマンドは原則カレントディレクトリを```cd ./pkgs```と移動した状態を前提としている。

## [Viewer起動・操作](./gui/vslam_viewer/README.md)

# Tips
## Enhance the 8cores
```bash
sudo nvpmodel -m 0
```

## submodules update
```bash
git submodule update --init --recursive &&\
git submodule update --recursive --force --checkout --remote
```

