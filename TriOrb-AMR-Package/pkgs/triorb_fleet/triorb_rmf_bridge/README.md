# Package: triorb_rmf_bridge

## Description
- 単体自律移動のFMS用Topicのバイパスを行う。
- ROS_LOCALHOST_ONLY=0と1のブリッジも担うため、global/local両方のコンテナで本パッケージを起動する必要がある。
- ブリッジ対象のtopicがglobal⇔localで無限ループする可能性がある場合は"RecentNSet<std::size_t>"を使った防御を行うこと。
- Global（FMS/上位管理システム）とLocal（ロボット）を跨いで送受信されるメッセージがあるとき、Global側のTopic名は末尾にHash値が付加されたメッセージを使う
```bash
    # Global（上位管理システム）側から見たメッセージ定義：
    Topic：(prefix)/drive/run_vel
    Type：triorb_drive_interface/msg/TriorbRunVel3
    # Local（ロボット）側から見たメッセージ定義：
    Topic：(prefix)/drive/run_vel
    Type：triorb_drive_interface/msg/TriorbRunVel3
```


## ROS2 Bypass Global to Local Topic

### マーカー座標系の目標位置
- Topic：(prefix)/drive/align_pos
- Type：triorb_drive_interface/msg/TriorbAlignPos3 

### ロボット座標系の目標速度
- Topic：(prefix)/drive/run_vel
- Type：triorb_drive_interface/msg/TriorbRunVel3

### Driving mode
- Topic：(prefix)/drive/set_mode
- Type：std_msgs/msg/String

### リフター動作指示
- Topic：(prefix)/drive/run_lifter
- Type：std_msgs/msg/String

### 停止指示
- Topic：(prefix)/drive/stop
- Type：std_msgs/msg/Empty

### ロボット座標系の目標位置
- Topic：(prefix)/drive/run_pos
- Type：triorb_drive_interface/msg/TriorbRunPos3

### アライメント開始
- Topic：(prefix)/drive/alignment/start
- Type：std_msgs/msg/String

### アライメント終了
- Topic：(prefix)/drive/alignment/terminate
- Type：std_msgs/msg/String

### FMS用watchdog
- Topic：(prefix)/fms_watchdog
- Type：std_msgs/msg/Int32

### 世界座標系の位置・姿勢へ向かう移動実行
- Topic：(prefix)/fms/set_pos
- Type：triorb_drive_interface/msg/TriorbSetPos3

### ロボットアームタスクの指令用
- Topic：(prefix)/arm_task_list
- Type：std_msgs/msg/String

### 拡張基盤用発進音声トピック
- Topic：(prefix)/ext_pico/start_auto_move
- Type：std_msgs/msg/Empty

### 拡張基盤用停止トピック
- Topic：(prefix)/ext_pico/end_auto_move
- Type：std_msgs/msg/Empty


## ROS2 Bypass Local to Global Topic

### 世界座標系の位置・姿勢
- Topic：(prefix)/vslam/rig_tf
- Type：geometry_msgs/msg/TransformStamped

### リフターState
- Topic：(prefix)/lifter/state
- std_msgs/msg/String

### リフターリザルト
- Topic：(prefix)/lifter/result
- std_msgs/msg/String

### 相対位置決めステータス配信
- Topic: (prefix)/drive/alignment/status
- Type: std_msgs/msg/String

### 相対位置決め結果配信
- Topic: (prefix)/drive/alignment/result
- Type: std_msgs/msg/String

### 自律移動完了結果配信
- Topic: (prefix)/drive/result
- Type: triorb_drive_interface/msg/TriorbRunResult

### ロボットウォッチドッグ配信
- Topic: (prefix)/amr_robot_watchdog
- Type: std_msgs/msg/String

### ロボットステータス配信
- Topic: (prefix)/robot/status
- Type: triorb_static_interface/msg/RobotStatus

### ホストステータス配信
- Topic: (prefix)/host/status
- Type: triorb_static_interface/msg/HostStatus

# パラメーター
- BRIDGE_IP : Global ⇔ Local ブリッジに使うIPアドレス（recommend: 127.0.0.1）
- BRIDGE_PORT_G2L : Global ⇒ Local ブリッジに使うポート (default 60000)
- BRIDGE_PORT_L2G : Global ⇒ Local ブリッジに使うポート (default 60001)