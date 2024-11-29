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

## Split bag file
```bash
sh dev_container.sh
tmux new-session -s record -d "source /install/humble/setup.bash && ros2 bag record -a -o {OUTPUT_BAG_PATH} -b 5153960755" # 4.8GB : 5153960755
ros2 bag play {INPUT_BAG_PATH} &&\
tmux send-keys -t record C-c
```