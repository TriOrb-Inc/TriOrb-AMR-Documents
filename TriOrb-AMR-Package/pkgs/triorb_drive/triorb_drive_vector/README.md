# Package: triorb_drive_vector

## Description
- 制御指令値からロボットの進行方向や停止・回転などの状態判定を行う。SLSやLED制御向け。
- 閾値設定はdrive_vector.xml

## Subscriber
### 移動指令を取得
- Topic: /drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage:

### 移動指令を取得
- Topic: /drive/run_vel
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage:

## Publisher
### 移動方向
- Topic: /drive/std_vector
- Type: Float32MultiArray
  - 配列フォーマット
  ```bash
  direction: 方向
  speed: 速度
  f_rotate: 時計回り 1 / 反時計回り -1
  f_stop: 停止と判定した際 1 / その他 -1
  ```

### ノードの動作開始通知
- Topic: (prefix)/_{ノード名}
- Type: std_msgs/msg/Empty

## Service
### ノードのバージョン情報を取得
- Topic: (prefix)/get/version/{ノード名}
- Type: triorb_static_interface/srv/Version

## Action
本パッケージではActionは利用していません。