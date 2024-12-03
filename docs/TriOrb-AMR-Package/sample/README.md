# TriOrb AMR 制御用サンプルプログラム

## Python Notebook

### [notebook/move_sample.ipynb](./notebook/move_sample.ipynb)

- ロボット座標系における移動指示（移動距離、回転量を送信）
- ロボット座標系における速度指示（並進速度、回転速度を送信）

### [notebook/slam_sample.ipynb](./notebook/slam_sample.ipynb)

- 世界座標系における現在位置姿勢の確認
- 世界座標系における移動指示（目標位置、姿勢を送信）
- 移動の中断指示

### [notebook/A_to_B_sample.ipynb](./notebook/A_to_B_sample.ipynb)

- 世界座標系における経由地点をリストに追加登録
- 経由地点の目標精度および移動速度を編集
- 経由地点リストを用いた自律移動の実行（経由地点を1つずつ送信）
- 経由地点リストの保存
- 経由地点リストの読込

### [notebook/navigate_action.ipynb](./notebook/navigate_action.ipynb)

- 世界座標系における経由地点をリストに追加登録
- 経由地点リストを用いた自律移動の実行（経由地点をまとめて送信し完了待ちする）
- 経由地点リストの保存
- 経由地点リストの読込
