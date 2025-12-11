# triorb_collab_lift

**パス**: `triorb_drive/triorb_collab_lift`  
**説明**: 協調グループからのリフター指示を各ロボットに配信し、結果を集約して完了可否を通知する協調リフト制御ノードです。

## triorb_collab_lift

協調グループからのリフター指示を各ロボットに配信し、結果を集約して完了可否を通知する協調リフト制御ノードです。

### Subscriber
#### 協調搬送対象ロボットの状態購読
- Topic: /collab/robot/status
- Type: std_msgs::msg::String

#### 協調リフト制御指令購読(本ロボットへ動作指示)
- Topic: /bc/collab/run_lifter
- Type: std_msgs::msg::String
- Message: "up", "down", "stop"

#### 協調リフト結果購読(各ロボットからの結果受信)
- Topic: /bc/collab/lifter/result
- Type: std_msgs::msg::String

### Publisher
#### 本Node情報をエラー監視モジュールに追加する
- Topic: /except_handl/node/add
- Type: std_msgs::msg::String

pub_run_lifter_
#### 協調リフト制御指令発行(本ロボットへ動作指示)
- Topic: /drive/run_lifter
- Type: std_msgs::msg::String
- Message: "up", "down", "stop"

#### 協調リフト結果発行(全ロボットのリフト操作結果を配信)
- Topic: /collab/lifter/result
- Type: std_msgs::msg::String

#### エラーを発行する
- Topic: /triorb/error/str/add
- Type: std_msgs::msg::String

#### 警告を発行する
- Topic: /triorb/warn/str/add
- Type: std_msgs::msg::String

