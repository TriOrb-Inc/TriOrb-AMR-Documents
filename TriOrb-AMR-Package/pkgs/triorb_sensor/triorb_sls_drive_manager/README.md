# Package: triorb_sls_drive_manager

## Description
- SLS(sick社製)のサンプルモジュール

## install & setup
- Ethernet通信 : サービスとして登録
- 進行方向の取得 : triorb_drive_vector
```bash
sudo bash ./setup.bash
```

## Subscriber
### ロボットへの絶対位置指示を受信
- Topic: (prefix)/drive/set_pos
- Type: triorb_drive_interface/msg/TriorbSetPos3

### 推定された運転ベクトル（進行方向・速度など）を受信
- Topic: (prefix)/drive/std_vector
- Type: std_msgs/msg/Float32MultiArray
- Usage: 進行方向のSLSのセンシング範囲を判断する為

### ロボット状態を受信（励磁やステータス等）
- Topic: (prefix)/robot/status
- Type: triorb_static_interface/msg/RobotStatus

## Publisher
### 一時停止指示(障害物検知)
- Topic: /drive/pause
- Type: std_msgs/msg/Empty

### 障害物消失時に自律走行再開指示を出す
- Topic: /drive/wakeup
- Type: std_msgs/msg/Empty

### 再始動指示
- Topic: /drive/restart
- Type: std_msgs/msg/Empty

### 速度制限
- Topic: /drive/speed_limit_by_safety_plc
- Type: std_msgs/msg/Float32

### ノードの動作開始通知
- Topic: (prefix)/_{ノード名}
- Type: std_msgs/msg/Empty

## Service
### ノードのバージョン情報を取得
- Topic: (prefix)/get/version/{ノード名}
- Type: triorb_static_interface/srv/Version

## Action
本パッケージではActionは利用していません。
