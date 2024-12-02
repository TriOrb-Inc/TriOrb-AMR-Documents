# Package: triorb_mutex_manager
- mutex管理およびTopicのバイパスを行う。
- ROS_LOCALHOST_ONLY=0と1のブリッジも担うため、global/local両方のコンテナで本パッケージを起動する必要がある。
- ブリッジ対象のtopicがglobal⇔localで無限ループする可能性がある場合は"RecentNSet<std::size_t>"を使った防御を行うこと。
- Global（上位管理システム）とLocal（ロボット）を跨いで送受信されるメッセージがあるとき、Global側のTopic名は末尾にHash値が付加されたメッセージを使う
- 末尾のHash値はmutexに使われるHashと一致させること
- なおHashは剛体Group内の全ロボットで共通のものではなく、ロボット固有のものとする。つまり、Sync move managerはロボット毎にトピックをPublish・Subscribeする必要がある。
```bash
    # Global（上位管理システム）側から見たメッセージ定義：
    Topic：(prefix)/drive/run_vel/sample_hash
    Type：triorb_drive_interface/msg/TriorbRunVel3
    # Local（ロボット）側から見たメッセージ定義：
    Topic：(prefix)/drive/run_vel
    Type：triorb_drive_interface/msg/TriorbRunVel3
```

# Global Publish
## mutex管理されているロボットのstate
- Topic：(prefix)/collab/mutex/state
- Type： std_msgs/msg/String
- Frequency : 1.0Hz
- Usage :
```bash
root@orin-nx-4260:/ws# ros2 topic echo /collab/mutex/state
data: '{"hash":"A0BA7E15","mutex":"lock"}'
```

## mutex管理されているロボットのresult
- Topic：(prefix)/collab/mutex/result
- Type： std_msgs/msg/String
- Usage :
```bash
```

# Global Subscribe and Response
## [Subscribe] mutexでlockされているか確認する
- Topic：(prefix)/collab/mutex/check_mutex
- Type：std_msgs/msg/Empty
- Usage：
```bash
```

## [Response] mutexでlockされているか
- Topic：(prefix)/collab/mutex/check_mutex/response
- Type：std_msgs/msg/String
- Usage：
```bash
```

## [Subscribe] mutex取得を試みてOKの場合はHASHを返却する（MUTEX_AUTO_RELEASE_MS秒以内にlock_mutexが呼ばれなければ自動開放する）
- Topic：(prefix)/collab/mutex/try_mutex
- Type： std_msgs/msg/Empty
- Usage：
```bash
```

## [Response] mutex取得を試みてOKの場合はHASHを返却する
- Topic：(prefix)/collab/mutex/try_mutex/response
- Type： std_msgs/msg/String
- Usage：
```bash
```

## [Subscribe] mutexを取得する
- Topic：(prefix)/collab/mutex/lock_mutex
- Type： std_msgs/msg/String
- Usage：
```bash
```

## [Response] mutexを取得する
- Topic：(prefix)/collab/mutex/lock_mutex/response
- Type： std_msgs/msg/String
- Usage：
```bash
```

## [Subscribe] mutexを解除する
- Topic：(prefix)/collab/mutex/unlock_mutex
- Type： std_msgs/msg/String
- Note： std_msgs/msg/String '{data: "force"}' # 強制全解除
- Usage：
```bash
ros2 topic pub /collab/mutex/unlock_mutex std_msgs/msg/String '{data: "force"}'
```

## [Response] mutexを解除する
- Topic：(prefix)/collab/mutex/unlock_mutex/response
- Type： std_msgs/msg/String
- Usage：
```bash
```

# ROS2 Passive Global Topic
## 現在のState
- Topic：(prefix)/collab/mutex/msg/collab_state
- Type：std_srvs/msg/String
- Usage：

# ROS2 Bypass Global to Local Topic
## 世界座標系の位置・姿勢へ向かう移動実行
- Topic(Global)：(prefix)/drive/set_pos/${Hash}
- Topic(Local)：(prefix)/drive/set_pos
- Type：triorb_drive_interface/msg/TriorbSetPos3
- Usage：

## マーカー座標系の目標位置
- Topic(Global)：(prefix)/drive/align_pos/${Hash}
- Topic(Local)：(prefix)/drive/align_pos
- Type：triorb_drive_interface/msg/TriorbAlignPos3
- Usage：

## ロボット座標系の目標速度
- Topic(Global)：(prefix)/drive/run_vel/${Hash}
- Topic(Local)：(prefix)/drive/run_vel
- Type：triorb_drive_interface/msg/TriorbRunVel3
- Usage：

## Driving mode
- Topic(Global)：(prefix)/drive/set_mode/${Hash}
- Topic(Local)：(prefix)/drive/set_mode
- Type：std_msgs/msg/String
- Usage：

## リフター動作指示
- Topic(Global)：(prefix)/drive/run_lifter/${Hash}
- Topic(Local)：(prefix)/drive/run_lifter
- Type：std_msgs/msg/String
- Usage：

# ROS2 Bypass Local to Global Topic

## 世界座標系の位置・姿勢
- Topic(Global)：(prefix)/vslam/rig_tf/${Hash}
- Topic(Local)：(prefix)/vslam/rig_tf 
- Type：geometry_msgs/msg/TransformStamped
- Usage：

## ナビゲーションリザルト
- Topic(Global)：(prefix)/collab/result/${Hash}
- Topic(Local)：(prefix)/collab/result
- std_msgs/msg/String
- Usage：

## リフターState
- Topic(Global)：(prefix)/lifter/state/${Hash}
- Topic(Local)：(prefix)/lifter/state
- std_msgs/msg/String
- Usage：

## リフターリザルト
- Topic(Global)：(prefix)/lifter/result/${Hash}
- Topic(Local)：(prefix)/lifter/result
- std_msgs/msg/String
- Usage：

# パラメーター
- BRIDGE_IP : Global ⇔ Local ブリッジに使うIPアドレス（recommend: 127.0.0.1）
- BRIDGE_PORT_G2L : Global ⇒ Local ブリッジに使うポート
- BRIDGE_PORT_L2G : Global ⇒ Local ブリッジに使うポート
- MUTEX_FILE : Mutex管理を行うファイル
- MUTEX_AUTO_RELEASE_MS : try_mutexの後lock_mutexが呼ばれなければmutex自動開放する時間[ms]
- PUBLISH_STATE_MS : mutex管理されているロボットのStateをPublishする時間間隔[ms]

# TODO
- Mutexの部分は一旦適当