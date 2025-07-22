# Package: triorb_drive_vector

## Description
- SLSやLED制御の為の進行方向を判断するモジュール
- ベースアルゴリズムはnavigation.cppを参考にした
- 閾値設定はdrive_vector.xmlで管理

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
- Usage: 
  - direction: 方向
  - speed: 速度
  - f_rotate: 時計回り 1 / 反時計回り -1
  - f_stop: 停止と判定した際 1 / その他 -1