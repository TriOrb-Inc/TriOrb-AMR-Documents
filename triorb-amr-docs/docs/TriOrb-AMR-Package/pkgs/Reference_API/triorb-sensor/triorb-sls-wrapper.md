# triorb_sls_wrapper

**パス**: `triorb_sensor/sick/triorb_sick_sls_wrapper`  
**説明**: 
    Convert SICK SLS RawMicroScanData topics into sensor_msgs/PointCloud messages.
  

## triorb_sls_wrapper

    Convert SICK SLS RawMicroScanData topics into sensor_msgs/PointCloud messages.
  

﻿# SICK SLS データツール

SICK SLS センサから取得した `raw_data.log` を可視化し、ROS 2 互換の占有グリッドへ変換する Python スクリプト群です。センサの検出補償範囲（minimum detectable free space）は 3.0 m と仮定し、+Inf を返したビームも走行可能領域として扱えます。

### 必要環境

- Python 3.9 以上
- [PyYAML](https://pyyaml.org/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Pillow](https://python-pillow.org/)（任意。PNG 出力に利用）

インストール例:

```bash
pip install pyyaml numpy matplotlib pillow
```

> Pillow が無い場合、`generate_occupancy.py` は Matplotlib を利用して PNG を保存します。

### /sick/raw_dataをサブスクライブしてPointCloudをPublishするノード（`src/raw_data_to_pointcloud_node.cpp`）
ROS 2 ノードとして動作し、`/sick/raw_data` トピックからデータを受信して、serial-numberが一致したデータをPointCloud2メッセージとしてパブリッシュします。オフセット値はミリメートル単位で指定します。シリアル番号ごとのキャリブレーション値は JSON ファイルにまとめて読み込み、`serial_number_of_device` に応じて自動で切り替わります。

`config/sls_point2d_config.json`（インストール後は`share/triorb_sls_wrapper/config/`配下）を編集してください:

```json
{
  "default": {
    "angle_offset": 0.0,
    "offset_x": 0.0,
    "offset_y": 0.0,
    "pointcloud_topic": "/sick/point2d"
  },
  "24050147": {
    "angle_offset": 290.0,
    "offset_x": 170.0,
    "offset_y": 156.0,
    "pointcloud_topic": "/sick/point2d47"
  },
  "24050160": {
    "angle_offset": 70.0,
    "offset_x": -170.0,
    "offset_y": 156.0,
    "pointcloud_topic": "/sick/point2d52"
  }
}
```

`pointcloud_topic` を省略した場合は `default` セクションの値が利用されます。`ROS_PREFIX` 環境変数が設定されている場合は接頭辞付きでトピックが生成されます。

```bash
colcon build && source install/setup.bash &&\
ros2 run triorb_sls_wrapper sls_point2d \
  --ros-args \
  -p config_file:=$(ros2 pkg prefix triorb_sls_wrapper)/share/triorb_sls_wrapper/config/sls_point2d_config.json
```

特定センサのみ処理したい場合は `-p serial_number:=<value>` と `-p filter_by_serial:=true` を併用してください。既定（`serial_number<=0`）では全シリアルを受け付け、JSONで定義されていないシリアルは `default` セクションの補正値が適用されます。

### /sick/raw_dataを占有グリッドへ変換するノード（`src/raw_data_to_occupancy_node.cpp`）

`/sick/raw_data` を購読し、スキャンごとに `nav_msgs/msg/OccupancyGrid` を生成してパブリッシュします。`generate_occupancy.py` のロジックをROS 2ノード化したもので、シリアル番号ごとに解像度や検知範囲、出力トピックを切り替えられます。

`config/sls_occupancy_config.json`（インストール後は`share/triorb_sls_wrapper/config/`配下）を編集してください:

```json
{
  "default": {
    "angle_offset": 0.0,
    "offset_x": 0.0,
    "offset_y": 0.0,
    "unit_scale": 0.001,
    "resolution": 0.05,
    "margin": 0.5,
    "xy_limit": 5.0,
    "detection_range": 10.0,
    "max_range": null,
    "beam_group_size": 4,
    "frame_id": "map",
    "occupancy_topic": "/sick/occupancy"
  },
  "24050160": {
    "angle_offset": 70.0,
    "offset_x": -170.0,
    "offset_y": 156.0,
    "xy_limit": 6.0,
    "beam_group_size": 4,
    "occupancy_topic": "/sick/occupancy52"
  }
}
```

`occupancy_topic` を省略した場合は `default` の値が利用されます。`ROS_PREFIX` 環境変数を指定すると接頭辞付きトピックへ自動変換されます。

`detection_range` は +Inf ビームに対しても自由セルとして扱う最大距離を表し、範囲内は占有率 0 で塗りつぶされます。`beam_group_size` は角度方向のビームをまとめる単位数で、各グループの中から最も近い障害物を含むビーム（なければ任意のビーム）が選択されるため、計算負荷を抑えつつ近距離の障害物を優先的に反映できます。

```bash
colcon build && source install/setup.bash &&\
ros2 run triorb_sls_wrapper sls_occupancy \
  --ros-args \
  -p config_file:=$(ros2 pkg prefix triorb_sls_wrapper)/share/triorb_sls_wrapper/config/sls_occupancy_config.json
```

`-p serial_number:=<value>` と `-p filter_by_serial:=true` を併用すれば、特定センサのみOccupancyGridを生成します。定義済みシリアルが1件だけの場合は自動でその設定が選択されます。

#### OccupancyGridをPNGとして保存するテストスクリプト

`test/save_occupancy_png.py` を利用すると、任意の占有グリッドトピックを購読して最初のメッセージをPNGとして保存できます。Pillow (`pip install pillow`) を事前にインストールしてください。

```bash
python3 test/save_occupancy_png.py \
  --topic /sick/occupancy52 \
  --output occupancy_snapshot.png
```

未知セル (-1) は灰、自由セル (0) は白、占有セル (100) は黒で描画されます。メッセージを1度受信すると自動的にノードが終了します。

### /sick/raw_dataをサブスクライブしてプロット（`plot_raw_data_node.py`）

パラメータは`plot_raw_data.py`と同様ですが、ROS 2 ノードとして動作し、`/sick/raw_data` トピックからデータを受信して、serial-numberが一致したデータをプロットします。オフセット値はミリメートル単位で指定します。

```bash
tmux new-session -s play -d "ros2 bag play -l test/rosbag2_2025_11_05-00_06_02/"
python plot_raw_data_node.py \
  --output raw_data_node_plot.svg \
  --serial-number 24050160 \
  --angle-offset 70 \
  --offset-x -170 \
  --offset-y 156
```

### raw_data のプロット (`plot_raw_data.py`)

極座標ビューと XY ビューを生成し、反射率つきでスキャン結果を確認します。オフセット値はミリメートル単位で指定します。

```bash
python plot_raw_data.py \
  --input raw_data.log \
  --output raw_data_plot.svg \
  --angle-offset 70 \
  --offset-x -170 \
  --offset-y 156 \
  --xy-limit 2000 \
  --dpi 1200
```

#### 主なオプション

- `--angle-offset` センサ取り付け角度の補正（度、時計回りが正）。
- `--offset-x`, `--offset-y` センサ位置の平行移動量（ミリメートル）。`offset-y` の正値で下方向にシフト。
- `--xy-limit` XY ビューの表示範囲（ミリメートル）。例: `2000` で ±2000 mm を描画。
- `--dpi` 画像保存時の解像度。高くすると詳細になるがファイルサイズも増加。
- `--show` 生成後に Matplotlib ウィンドウを表示。

Polar View には 0.1 ステップの補助円を追加、XY View は等倍率で描画します。

### 占有グリッド生成 (`generate_occupancy.py`)

`raw_data.log` から ROS 2 `nav_msgs::msg::OccupancyGrid` 互換の PNG と JSON メタデータを出力します。センサオフセットはミリメートル、その他の距離系はメートルで指定します。

```bash
python generate_occupancy.py \
  --input raw_data.log \
  --output occupancy_map.png \
  --output-meta occupancy_map.json \
  --resolution 0.03 \
  --unit-scale 0.001 \
  --angle-offset 70 \
  --offset-x -170 \
  --offset-y 156 \
  --infinite-free-range 3.0 \
  --detection-range 10.0 \
  --xy-limit 5.0 \
  --dpi 600
```

#### 主なパラメータ

- `--resolution` グリッド解像度（メートル/セル）。既定値は 0.01。
- `--unit-scale` 距離の単位変換。ミリ -> メートルなら 0.001。
- `--xy-limit` センサ中心の正方形領域を ±値メートルでクリップ。未指定ならスキャン範囲に余白を加えて自動計算。
- `--margin` `--xy-limit` 未指定時に周囲へ加える余白（メートル）。
- `--max-range` 指定距離を超える計測値を除外（メートル）。
- `--angle-offset` 角度補正（度）。`plot_raw_data.py` と同じ値を推奨。
- `--offset-x`, `--offset-y` センサ位置の補正量（ミリメートル）。内部で `unit-scale` によりメートルへ換算。
- `--infinite-free-range` +Inf（飽和）ビームに対して最低限走行可能とみなす距離（メートル）。既定値は 3.0 m（SICK 検出補償範囲）。
- `--detection-range` 3.0 m から 10.0 m までを検出可能範囲とみなし、距離に応じて占有率 0~50 を割り当てます。
- `--output-meta` ROS 用メタデータ (JSON) を保存。
- `--show` Matplotlib を使って占有グリッドを表示。

#### 出力

- **occupancy_map.png**: 占有セル (100) は黒、自由セル (0) は白、未知セル (-1) は灰。画像は ROS の座標系に合わせて下向き原点で保存。
- **occupancy_map.json**: `resolution`、`width`、`height`、`origin` など `nav_msgs::msg::OccupancyGrid::info` に転記可能な情報を含む。

ROS 2 側では画像を行優先（row-major）で読み込み、`origin` を踏まえて `data` 配列へ展開してください。

### 運用のヒント

- 角度・平行移動オフセットは両スクリプトで統一すると結果が揃います。
- 高 DPI 設定はファイルサイズが大きくなるため用途に応じて調整してください。
- `--max-range` や `--infinite-free-range` を活用して、走行可能領域の解像度と範囲のバランスを取ってください。

