# Package: triorb_parallel_move_manager
- 協調搬送における各ロボット独立制御を管理する
- タスクの情報を受け取り、他のモジュールへキャストする
- ステートの管理および逐次実行を把握しPublishする

# Request definition
```bash
{
    name : sample_job_001
    mode : pararell_move / pararell_into / pararell_outof
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
### Parallel moveのState
- Topic: (prefix)/collab/parallel/state
- Type: std_msgs/msg/String
- Frequency: 1.0Hz
- Usage: 
```bash
```

### Parallel moveのResult
- Topic: (prefix)/collab/parallel/result
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

### 潜り込みのリクエスト
- Topic: (prefix)/collab/into/request
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 離脱のリクエスト
- Topic: (prefix)/collab/outof/request
- Type: std_msgs/msg/String
- Usage: 
```bash
```

## Subscriber
### Parallel moveのリクエスト
- Topic: (prefix)/collab/parallel/request
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### Parallel moveのリクエスト
- Topic: (prefix)/collab/parallel/terminate
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 移動のState
- Topic: (prefix)/collab/move/state
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 潜り込みのState
- Topic: (prefix)/collab/into/state
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 離脱のState
- Topic: (prefix)/collab/outof/state
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 移動のResult
- Topic: (prefix)/collab/move/result
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 潜り込みのResult
- Topic: (prefix)/collab/into/result
- Type: std_msgs/msg/String
- Usage: 
```bash
```

### 離脱のResult
- Topic: (prefix)/collab/outof/result
- Type: std_msgs/msg/String
- Usage: 
```bash
```

