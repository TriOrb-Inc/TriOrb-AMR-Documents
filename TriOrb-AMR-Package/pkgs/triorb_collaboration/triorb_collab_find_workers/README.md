# Package: triorb_collab_find_workers

| 入力                                                                   | 条件                                                                  | 出力                                                                     |
| :--------------------------------------------------------------------- | :-------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| （上からユニキャストで）Jobを実行するWorkerを選定してください※ Job情報 | -                                                                     | （ロボットへブロードキャストで）Jobにアサイン可能か問い合わせ            |
| ^                                                                      | 5秒待って、図書館で登録されているWorkerから可能との回答が揃った場合   | （Job state managerへ）Jobを実施/管理してください。※ Job情報・Worker情報 |
| ^                                                                      | ^                                                                     | （該当のロボットへ）排他制御を実施してください※ Job ID                   |
| ^                                                                      | 1分待っても、図書館で登録されているWorkerから可能との回答がない場合   | （上へ）Workerを見つけることができませんでした/Workerがいない            |
| （Job state managerから）すべてのWorkerの排他制御を解除してください    | -                                                                     | （ロボットへブロードキャストで）排他制御を解除してくだい                 |
| ^                                                                      | すべてのWorkerから”排他制御の解除完了”の信号が来るのを待つ            | -                                                                        |
| ^                                                                      | 1分待ち続けても、すべてのWorkerから”排他制御の解除完了”の信号が来ない | （もう一度、排他制御の解除指示を出してみる、など）                       |
| ^                                                                      | ^                                                                     | （Job state managerへ）Workerの排他制御の解除が完了できませんでした      |
| ^                                                                      | すべてのWorkerから”排他制御の解除完了”の信号が来た                    | （Job state managerへ）すべてのWorkerの排他制御の解除が完了しました      |
| （ロボットから）アサイン可能※ ロボット名・命令Hash                     | -                                                                     | -                                                                        |
| （ロボットから）排他制御の解除完了※ ロボット名・命令Hash               | -                                                                     | -                                                                        |

# Subscriber
## Jobの開始要求
- Topic：(prefix)/collab/find/create
- Type：std_msgs/msg/String
- Definition：
```bash
{
    job_name : (jobの名前),
    task_name : (taskの名前),
    worker_num : 2
    robot : # 将来的には空でも良い
    [
        (Robot1のhostname),
        (Robot2のhostname)
    ],
    map : # 空でも良い
    {
        name : (地図ファイル名),
        ip : (地図ファイルを持っているロボットのIPアドレス)
    },
    task_info : 
    [
        {
            mode : (動きの種別 ex. pararell_move),
            move : 
            [
                {
                    route : (ロボット1の移動経路情報)
                },
                {
                    route : (ロボット2の移動経路情報)
                }
            ]
        },
        {
            mode : (動きの種別 ex. pararell_into),
            move : 
            [
                {
                    route : (ロボット1の移動経路情報)
                },
                {
                    route : (ロボット2の移動経路情報)
                }
            ]
        },
        {
            mode : (動きの種別 ex. sync_lift),
            direction : (リフターUP/Down),
        },
        {
            mode : (動きの種別 ex. sync_move),
            route : (荷物の移動経路情報)
        },
        {
            mode : (動きの種別 ex. sync_lift),
            route : (リフターUP/Down)
        },
        {
            mode : (動きの種別 ex. pararell_outof),
            move : 
            [
                {
                    route : (ロボット1の移動経路情報)
                },
                {
                    route : (ロボット2の移動経路情報)
                }
            ]
        }
    ]
}
```
- Usage：
```bash
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/find/create std_msgs/msg/String "{data: '{\
    "'"job_name"'" : "'"sample_job_001"'",\
    "'"task_name"'" : "'"sample_task"'",\
    "'"robot"'" : \
    [\
        "'"orin-nx-4944"'",\
        "'"orin-nx-4260"'"\
    ],\
    "'"task_info"'" : \
    [\
        {\
            "'"mode"'" : "'"pararell_move"'",\
            "'"move"'" : \
            [\
                {\
                    "'"robot"'" : "'"A4298950"'",\
                    "'"route"'" : []\
                }\
            ]\
        },\
        {\
            "'"mode"'" : "'"pararell_into"'",\
            "'"move"'" : \
            [\
                {\
                    "'"robot"'" : "'"A4298950"'",\
                    "'"route"'" : []\
                }\
            ]\
        },\
        {\
            "'"mode"'" : "'"sync_lift"'",\
            "'"direction"'" : "'"up"'"\
        }\
    ]\
}'}"
```

## Jobの終了要求
- Topic：(prefix)/collab/find/terminate
- Type：std_msgs/msg/String
- Usage：
```bash
root@orin-nx-4260:/ws# ros2 topic pub /collab/find/terminate std_msgs/msg/String "{data: sample_job_001}"
```

## mutex取得試みの結果を取得する
- Topic：(prefix)/collab/mutex/try_mutex/response
- Type： std_msgs/msg/String


# Publisher
## Jobの開始要求Result
- Topic：(prefix)/collab/find/create/result
- Type：std_msgs/msg/String
- Usage：
```bash
```

## Jobの終了要求Result
- Topic：(prefix)/collab/find/terminate/result
- Type：std_msgs/msg/String
- Usage：
```bash
```

## mutex取得を試みる
- Topic：(prefix)/collab/mutex/try_mutex
- Type： std_msgs/msg/Empty
- Usage：


# パラメーター
- TIMEOUT_MS_CREATE : 開始要求してからロボットが発見できなかったとして諦めるまでの時間 [ms]
- TIMEOUT_MS_TERMINATE : 終了要求してから終了処理できなかったとして諦めるまでの時間 [ms]

# Unit Test
```bash
root@orin-nx-4944:/ws# source /install/${ROS_DISTRO}/setup.bash
root@orin-nx-4944:/ws# tmux new-session -s find -d "colcon build --packages-select triorb_collab_find_workers && source install/setup.bash && ros2 run triorb_collab_find_workers collab_find_workers"
root@orin-nx-4944:/ws# tmux new-session -s start -d "source install/setup.bash && ros2 topic echo -f /collab/group/create std_msgs/msg/String"
root@orin-nx-4944:/ws# ros2 topic pub -1 /collab/find/create std_msgs/msg/String "{data: '{\
    "'"job_name"'" : "'"sample_job_001"'",\
    "'"task_name"'" : "'"sample_task"'",\
    "'"robot"'" : \
    [\
        "'"orin-nx-4944"'",\
        "'"orin-nx-4260"'"\
    ],\
    "'"task_info"'" : \
    [\
        {\
            "'"mode"'" : "'"pararell_move"'",\
            "'"move"'" : \
            [\
                {\
                    "'"robot"'" : "'"orin-nx-4944"'",\
                    "'"route"'" : []\
                }\
            ]\
        },\
        {\
            "'"mode"'" : "'"pararell_into"'",\
            "'"move"'" : \
            [\
                {\
                    "'"robot"'" : "'"orin-nx-4944"'",\
                    "'"route"'" : []\
                },\
                {\
                    "'"robot"'" : "'"orin-nx-4260"'",\
                    "'"route"'" : []\
                }\
            ]\
        },\
        {\
            "'"mode"'" : "'"sync_lift"'",\
            "'"direction"'" : "'"up"'"\
        }\
    ]\
}'}"
root@orin-nx-4944:/ws# tmux a -t start
data: '{"job_name":"sample_job_001","robot":["h0fbeb0c","h74e2412"],"task_info":[{"mode":"pararell_move","move":[{"robot":"h0fbeb0c","route":[]}]},{"mode":"pararell_into","move":[{"robot":"h0fbeb0c","route":[]},{"robot":"h74e2412","route":[]}]},{"direction":"up","mode":"sync_lift"}],"task_name":"sample_task","workers":["h0fbeb0c","h74e2412"]}'
---
```