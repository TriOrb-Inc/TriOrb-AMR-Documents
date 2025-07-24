# Package: triorb_dead_reckoning
## Package Description
- IMU・オドメトリ・VSLAMデータを統合し、iSAM2グラフ最適化を用いたデッドレコニングによる自己位置推定を行うROS2ノードです。推定結果はトピック配信、デバッグモードでCSVログの出力をします。

## Subscriber
### オドメトリデータを受信して自己位置推定に利用
- Topic: (prefix)/triorb/odom
- Type: geometry_msgs/msg/Vector3Stamped

### VSLAM推定姿勢データを受信して自己位置推定に利用
- Topic: (prefix)/vslam/rig_tf
- Type: geometry_msgs/msg/TransformStamped

## Publisher
### デッドレコニング推定結果を配信
- Topic: (prefix)/triorb/dead_reckoning
- Type: geometry_msgs/msg/Vector3Stamped

### ノードの動作開始通知
- Topic: (prefix)/_{ノード名}
Type: std_msgs/msg/Empty

## Service
### ノードのバージョン情報を取得
- Topic: (prefix)/get/version/{ノード名}
- Type: triorb_static_interface/srv/Version

## Action
本パッケージではActionは利用していません。

## MQTT
### id
- triorb_dead_reckoning_stream_{random.randint(0, 10000)}
### Publish
- Topic: /dead_reckoning/stream
    - jeson format
    ```bash
    {
    "imu_acc":[x,x,z]
    "imu_gyro":[x,x,z]
    "odometry":[x,x,w]
    "vslam":[x,x,w]
    "gtsam":[x,x,w]
    "serial_status":"状態をstring"
    "vslam_off":"状態をTrue/False"
    }
    ```
### Subscribe
- Topic: /dead_reckoning/debug/start
    - デバッグモード開始 Emptyメッセージ
- Topic: /dead_reckoning/debug/end
    - デバッグモード終了 Emptyメッセージ
- Topic: /dead_reckoning/vslam/off
    - vslam/rig_tfを無視 Emptyメッセージ