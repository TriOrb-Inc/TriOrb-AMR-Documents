# Package: triorb_sync_move_manager
- 協調搬送における各ロボット協調制御を管理する
- タスクの情報を受け取り、他のモジュールへキャストする
- ステートの管理および逐次実行を把握しPublishする

# Request definition
```bash
{
    name : sample_job_001
    mode : sync_lift / sync_move
    direction : up / down
    move : [
        {
            robot : (ロボット1のHash),
            route : (ロボット1の移動経路情報)
        },
        {
            robot : (ロボット2のHash),
            route : (ロボット2の移動経路情報)
        },
    ]
}
```

## Publisher
### Sync moveのState
- Topic: (prefix)/collab/sync/state
- Type: std_msgs/msg/String
- Frequency: 1.0Hz
- Usage: 
```bash
```

### Sync moveのResult
- Topic: (prefix)/collab/sync/result
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### Lifter startのリクエスト
- Topic: (prefix)/collab/lifter/start/request
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 移動のリクエスト
- Topic: (prefix)/collab/move/request
- Type: std_msgs/msg/String
- Usage: 
```bash
```

## Subscriber
### Sync moveのリクエスト
- Topic: (prefix)/collab/sync/request
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### Sync moveの完了
- Topic: (prefix)/collab/sync/terminate
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### リフターのState
- Topic: (prefix)/collab/lifter/state
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 協調移動のState
- Topic: (prefix)/collab/move/state
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### リフターのResult
- Topic: (prefix)/collab/lifter/result
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 協調移動のResult
- Topic: (prefix)/collab/move/result
- Type: std_msgs/msg/String
- Usage: 
```bash
```

## [triorb_sync_move_manager Types](../TriOrb-ROS2-Types/triorb_sync_move_manager/README.md)
