# triorb_collab_lift

**パス**: `triorb_drive/triorb_collab_lift`  
**説明**: 複数のAMRによる協調リフト制御を提供するパッケージです。複数ロボット間でリフト動作を同期し、安全かつ安定的に荷物を持ち上げることを目的としています。

## Package: triorb_collab_lift

このパッケージは、複数のAMR（自律移動ロボット）による協調リフト制御を提供します。ロボット間の動作を同期させることで、荷物を安定かつ安全に持ち上げることができます。

### 主な機能

- 複数ロボットのリフト動作の同期制御
- 荷物持ち上げ時の姿勢安定化
- リフト完了時の信号通知

---

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

