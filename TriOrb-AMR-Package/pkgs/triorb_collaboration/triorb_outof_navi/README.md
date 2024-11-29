# Package: triorb_outof_navi
- 離脱を実行する
- 離脱開始命令を受け取り、ロボットに命令を伝達する

|入力|条件|出力|
|:--|:--|:--|
|離脱を開始してください※荷物のWaypoints・荷物中心から各ロボット中心の相対姿勢|-|（ロボットへブロードキャストで）○○の速度で潜り込んでください|
|（ロボットから）離脱しました|1. すべてのWorkerから”離脱完了”の信号が来るのを待つ|-|
|^|2. 1分待ち続けても信号が来ない|（もう一度、離脱指示を出してみる、など）|
|^|^|（上へ）離脱することができませんでした|
|^|3. すべてのWorkerから”離脱完了”の信号が来た|（上へ）離脱が完了しました|

# Parameter
- KEEP_WAITING_TIME_MS : 離脱完了待ち時間 [ms]（これを過ぎたら失敗通知する）

# Requirement definition
```bash
{
    robot : (ロボットのHash),
    route : [
        {
            acc : (加速時間 time [ms]), # 任意。設定が無ければプリセットを使う
            dec : (加速時間 time [ms]), # 任意。設定が無ければプリセットを使う
            vel_xy_max : (ロボットの最大並進速度　[m/s]), # 任意。設定が無ければプリセットを使う
            vel_w_max : (ロボットの最大回転速度　[rad/s]), # 任意。設定が無ければプリセットを使う
            tags_pose : [
                {
                    id : (tag id), # Tag1のID
                    pose_goal2tag : [(x),(y),(yaw)] # Goal座標系におけるタグ1の位置・姿勢
                },
                {
                    id : (tag id), # Tag2のID
                    pose_goal2tag : [(x),(y),(yaw)] # Goal座標系におけるタグ2の位置・姿勢
                },
                {
                    id : (tag id), # Tag3のID
                    pose_goal2tag : [(x),(y),(yaw)] # Goal座標系におけるタグ3の位置・姿勢
                }
            ]
        }, # 離脱完了位置の相対位置決め
    ] # 離脱時の経由地点も設定できるようリストにしている
},
```

# Subscriber
## 離脱開始Request
- Topic: (prefix)/collab/out/request
- Type： std_msgs/msg/String

## 相対位置決めStatus
- Topic: (prefix)/drive/alignment/status/(Hash)
- Type： std_msgs/msg/String

## 相対位置決めResult
- Topic: (prefix)/drive/alignment/result/(Hash)
- Type： std_msgs/msg/String

# Publither
## 相対位置決め開始Request
- Topic: (prefix)/drive/alignment/start/(Hash)
- Type： std_msgs/msg/String

## 相対位置決め終了Request
- Topic: (prefix)/drive/alignment/terminate/(Hash)
- Type： std_msgs/msg/String

## 離脱Status
- Topic: (prefix)/collab/out/status
- Type： std_msgs/msg/String
- Frequency: 1.0Hz

## 離脱Result
- Topic: (prefix)/collab/out/result
- Type： std_msgs/msg/String


## [triorb_outof_navi Types](../TriOrb-ROS2-Types/triorb_outof_navi/README.md)