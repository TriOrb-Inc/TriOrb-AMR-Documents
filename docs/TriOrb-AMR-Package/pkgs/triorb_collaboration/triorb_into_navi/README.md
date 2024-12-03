# Package: triorb_into_navi
- 潜り込みを実行する
- 潜り込み開始命令を受け取り、ロボットに命令を伝達する

|入力|条件|出力|
|:--|:--|:--|
|潜り込みを開始してください※荷物のWaypoints・荷物中心から各ロボット中心の相対姿勢|-|（ロボットへブロードキャストで）○○の速度で潜り込んでください|
|（ロボットから）潜り込みました|1. すべてのWorkerから”潜り込み完了”の信号が来るのを待つ|-|
|^|2. 1分待ち続けても信号が来ない|（もう一度、潜り込み指示を出してみる、など）|
|^|^|（上へ）潜り込むことができませんでした|
|^|3. すべてのWorkerから”潜り込み完了”の信号が来た|（上へ）潜り込みが完了しました|

# Parameter
- KEEP_WAITING_TIME_MS : 潜り込み完了待ち時間 [ms]（これを過ぎたら失敗通知する）

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
        }, # 潜り込み開始位置の相対位置決め
        {
            tags_pose : [
                {
                    id : (tag id), # Tag4のID
                    pose_goal2tag : [(x),(y),(yaw)] # Goal座標系におけるタグ4の位置・姿勢
                },
                {
                    id : (tag id), # Tag5のID
                    pose_goal2tag : [(x),(y),(yaw)] # Goal座標系におけるタグ5の位置・姿勢
                },
                {
                    id : (tag id), # Tag6のID
                    pose_goal2tag : [(x),(y),(yaw)] # Goal座標系におけるタグ6の位置・姿勢
                }
            ]
        } # 潜り込み完了位置の相対位置決め
    ] # 潜り込み時の経由地点も設定できるようリストにしている
},
```

# Subscriber
## 潜り込み開始Request
- Topic: (prefix)/drive/into/start
- Type： std_msgs/msg/String

## 潜り込み終了Request
- Topic: (prefix)/drive/into/terminate
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

## 潜り込みStatus
- Topic: (prefix)/drive/into/status
- Type： std_msgs/msg/String
- Frequency: 1.0Hz

## 潜り込みResult
- Topic: (prefix)/drive/into/result
- Type： std_msgs/msg/String
