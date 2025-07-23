# triorb_collab_navi

このパッケージは、複数のAMRによる協調搬送中のナビゲーションを担当します。干渉を避けながら、各ロボットが協調して目的地まで搬送を行えるよう支援します。

## 主な機能

- 経路計画と経路追従
- 衝突回避と速度調整
- 複数ロボット間の同期ナビゲーション

---

## Subscriber
### 経路追従制御の開始命令
- Topic: /drive/init_path_follow
- Type: std_msgs::msg::Empty

### 一時停止/再開/停止
- Topic: /drive/pause, /drive/resume, /drive/stop
- Type: std_msgs::msg::Empty

## Publisher
### 搬送完了通知
- Topic: /collab/drive/finish
- Type: std_msgs::msg::Empty

### 姿勢共有情報
- Topic: /collab/group_pose
- Type: geometry_msgs::msg::PoseArray

### 本Node情報をエラー監視モジュールに追加する
- Topic: /except_handl/node/add
- Type: std_msgs::msg::String

### エラーを発行する
- Topic: /triorb/error/str/add
- Type: std_msgs::msg::String

### 警告を発行する
- Topic: /triorb/warn/str/add
- Type: std_msgs::msg::String
