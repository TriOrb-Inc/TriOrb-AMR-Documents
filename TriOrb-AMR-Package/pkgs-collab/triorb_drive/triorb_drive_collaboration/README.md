# triorb_drive_collaboration

このパッケージは、複数AMRによる協調搬送タスクを統合的に管理するフレームワークです。リフト・ナビゲーション・ポーズ推定などの各機能を統括し、効率的な搬送を実現します。

## 主な機能

- 協調搬送プロセスの統合管理
- 各機能パッケージとの連携
- 実行のためのLaunchファイル提供

---

## Subscriber
### 各ロボットの入力（ジョイ、状態など）
- Topic: /collab/joy, /collab/sleep, /collab/wakeup
- Type: sensor_msgs::msg::Joy / std_msgs::msg::Empty

## Publisher
### 実行速度の指令
- Topic: /collab/run_vel
- Type: geometry_msgs::msg::Twist

### リフト動作の指令
- Topic: /collab/run_lifter
- Type: std_msgs::msg::String

### 本Node情報をエラー監視モジュールに追加する
- Topic: /except_handl/node/add
- Type: std_msgs::msg::String

### エラーを発行する
- Topic: /triorb/error/str/add
- Type: std_msgs::msg::String

### 警告を発行する
- Topic: /triorb/warn/str/add
- Type: std_msgs::msg::String
