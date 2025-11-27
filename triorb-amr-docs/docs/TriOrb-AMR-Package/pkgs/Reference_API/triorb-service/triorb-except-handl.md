# triorb_except_handl

**パス**: `triorb_service/triorb_except_handl`  
**説明**: TODO: Package description

## Package: triorb_except_handl
### Config
#### config/node_check.json
- node_list: 存在しない場合ERRORとするnode名を記入(string)
    - /except_handl/node/add トピックから追記可能
    - /except_handl/node/remove トピックから削除可能
- delay_sec: Node監視の開始遅延時間(float)[s]

#### config/${node_name}_restart.sh
nodeが存在しなかった場合にホスト側で実行するshell script

### Subscriber
#### エラーの受取り
- Topic: (prefix)/triorb/error/add
- Type: std_msgs::msg::UInt16
- Usage:
```bash
ros2 topic pub --once /triorb/error/add std_msgs/msg/UInt16 '{"data":49}'
```

#### エラーの受取り（任意文字列版）
- Topic: (prefix)/triorb/error/str/add
- Type: std_msgs::msg::String
- Usage:
```bash
ros2 topic pub --once /triorb/error/str/add std_msgs/msg/String '{"data": "Sample error message"}'
```

#### 警告の受取り
- Topic: (prefix)/triorb/warn/add
- Type: std_msgs::msg::UInt16
- Usage:
```bash
ros2 topic pub --once /triorb/warn/add std_msgs/msg/UInt16 '{"data":1}'
```

#### 警告の受取り（任意文字列版）
- Topic: (prefix)/triorb/warn/str/add
- Type: std_msgs::msg::String
- Usage:
```bash
ros2 topic pub --once /triorb/warn/str/add std_msgs/msg/String '{"data": "Sample warning message"}'
```

#### エラーリセットの実行
- Topic: (prefix)/triorb/error/reset
- Type: std_msgs/msg/Uint8
- Usage: 
```bash
ros2 topic pub --once /triorb/error/reset std_msgs/msg/UInt8 '{"data":1}' # dataが1以上のときリセット実行
```

#### 監視対象ノード追加
- Topic: (prefix)/except_handl/node/add
- Type: std_msgs/msg/String
- Usage: 
```bash
ros2 topic pub --once /except_handl/node/add std_msgs/msg/String '{"data":"sample_node"}'
```

#### 監視対象ノード削除
- Topic: (prefix)/except_handl/node/remove
- Type: std_msgs/msg/String
- Usage: 
```bash
ros2 topic pub --once /except_handl/node/remove std_msgs/msg/String '{"data":"sample_node"}'
```

### Publisher
#### エラー履歴の発行
- Topic: (prefix)/triorb/error/log
- Type: std_msgs::msg::UInt16MultiArray
 - 例:
```bash
ros2 topic echo --once /triorb/error/log
data:
- 32
- 49
```

#### エラー履歴の発行（文字列版）
- Topic: (prefix)/triorb/error/str/log
- Type: std_msgs::msg::String
- Format: 1件1行の平文
 - 例:
```bash
ros2 topic echo --once /triorb/error/str/log
data: "sensor timeout"
```

#### 警告履歴の発行
- Topic: (prefix)/triorb/warn/log
- Type: std_msgs::msg::UInt16MultiArray
 - 例:
```bash
ros2 topic echo --once /triorb/warn/log
data:
- 1
```

#### 警告履歴の発行（文字列版）
- Topic: (prefix)/triorb/warn/log
- Type: std_msgs::msg::String
- Format: 1件1行の平文
 - 例:
```bash
ros2 topic echo --once /triorb/warn/log
data: "map outdated"
```

#### エラー件数の発行
- Topic: (prefix)/triorb/error/num
- Type: std_msgs::msg::UInt8
 - 例:
```bash
ros2 topic echo --once /triorb/error/num
data: 2
```

#### 警告件数の発行
- Topic: (prefix)/triorb/warn/num
- Type: std_msgs::msg::UInt8
 - 例:
```bash
ros2 topic echo --once /triorb/warn/num
data: 1
```

