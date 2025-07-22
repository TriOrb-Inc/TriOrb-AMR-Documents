# Package: triorb_job_state_manager
- Jobおよびロボットの管理を行う
- Jobのcreate要求が来たタイミングでMutexの取得、Parallel move managerとの接続、Sync move managerとの接続を行う
- Jobのterminate要求/Compleatのタイミングで上記Mutexの解放と接続の切断を行う

## Publisher
### 剛体グループ（Job）のState
- Topic: (prefix)/collab/group/state
- Type: std_msgs/msg/String
- Frequency: 1.0Hz
- Usage: 
```bash
root@orin-nx-4260:/ws# ros2 topic echo /collab/group/state --full-length
data: '{"state": "in progress (1/3)", "managed_workers": ["A4298950"], "in_progress": "{\"mode\": \"pararell_move\", \"move\": [{\"robot\": \"A4298950\", \"route\": []}]}"}'
```
### 剛体グループ（Job）のResult
- Topic: (prefix)/collab/group/result
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### Parallel moveのリクエスト
- Topic: (prefix)/collab/parallel/request
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### Parallel moveの終了リクエスト
- Topic: (prefix)/collab/parallel/terminate
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### Sync moveのリクエスト
- Topic: (prefix)/collab/sync/request
- Type: std_msgs/msg/String
- Usage: 
```bash
```

## Subscriber
### 剛体グループ（Job）を終了削除する
- Topic: (prefix)/collab/stop
- Type： std_msgs/msg/String
- Usage：
```bash
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/stop std_msgs/msg/String "{data:'sample_job_001'}"
```

### Parallel moveのStaet
- Topic: (prefix)/collab/parallel/state
- Type: std_msgs/msg/String
- Usage: 
```bash
```
### Parallel moveのResult
- Topic: (prefix)/collab/parallel/result
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### Sync moveのStaet
- Topic: (prefix)/collab/sync/state
- Type: std_msgs/msg/String
- Usage: 
```bash
```
### Sync moveのResult
- Topic: (prefix)/collab/sync/result
- Type: std_msgs/msg/String
- Usage: 
```bash
```

## Service
### 剛体グループ（Job）を新規作成する
- Topic: (prefix)/collab/group/create
- Type: triorb_static_interface/srv/SetString
- JSON description: 
```bash
{
    job_name : (jobの名前),
    task_name : (taskの名前),
    workers : 
    [
        (Robot1のHash),
        (Robot2のHash)
    ],
    map : 
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
                    robot : (ロボット1のHash),
                    route : (ロボット1の移動経路情報)
                },
                {
                    robot : (ロボット2のHash),
                    route : (ロボット2の移動経路情報)
                }
            ]
        },
        {
            mode : (動きの種別 ex. pararell_into),
            move : 
            [
                {
                    robot : (ロボット1のHash),
                    route : (ロボット1の移動経路情報)
                },
                {
                    robot : (ロボット2のHash),
                    route : (ロボット2の移動経路情報)
                }
            ]
        },
        {
            mode : (動きの種別 ex. sync_lift),
            direction : (リフターUP/Down),
            workers : [
                (Robot1のHash),
                (Robot2のHash)
            ]
        },
        {
            mode : (動きの種別 ex. sync_move),
            route : (荷物の移動経路情報)
            workers : [
                (Robot1のHash),
                (Robot2のHash)
            ]
        },
        {
            mode : (動きの種別 ex. sync_lift),
            route : (リフターUP/Down)
            workers : [
                (Robot1のHash),
                (Robot2のHash)
            ]
        },
        {
            mode : (動きの種別 ex. pararell_outof),
            move : 
            [
                {
                    robot : (ロボット1のHash),
                    route : (ロボット1の移動経路情報)
                },
                {
                    robot : (ロボット2のHash),
                    route : (ロボット2の移動経路情報)
                }
            ]
        }
    ]
}
```
- Usage: 
```bash
root@orin-nx-4260:/ws# ros2 service call /collab/group/create triorb_static_interface/srv/SetString \
"{request: {'{\
    "'"job_name"'" : "'"sample_job_001"'",\
    "'"task_name"'" : "'"sample_task"'",\
    "'"workers"'" : \
    [\
        "'"A4298950"'"\
    ],\
    "'"map"'" : \
    {\
        "'"name"'" : "'"sample_map.sqlite3"'",\
        "'"ip"'" : "'"192.168.21.26"'"\
    },\
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
}'}}"

requester: making request: triorb_static_interface.srv.SetString_Request(request=['{    "job_name" : "sample_job_001",    "task_name" : "sample_task",    "workers" :     [        "A4298950"    ],    "map" :     {        "name" : "sample_map.sqlite3",        "ip" : "192.168.21.26"    },    "task_info" :     [        {            "mode" : "pararell_move",            "move" :             [                {                    "robot" : "A4298950",                    "route" : []                }            ]        },        {            "mode" : "pararell_into",            "move" :             [                {                    "robot" : "A4298950",                    "route" : []                }            ]        },        {            "mode" : "sync_lift",            "direction" : "up"        }    ]}'])

response:
triorb_static_interface.srv.SetString_Response(result='success')
```

# パラメーター
- PUBLISH_STATE_FREQ_MS : SteteをPublishする時間間隔[ms]
- STATE_MANAGEMENT_FREQ_MS : Stateを管理する時間間隔[ms]
- NO_STATUS_TIMEOUT : ステータスが返ってこない場合にタイムアウト判断する時間 [ms]