# 協調移動 API Reference v1.2.0 (2025-07-17)

## Package: triorb_drive_collaboration

このパッケージは、複数AMRによる協調搬送タスクを統合的に管理するフレームワークです。リフト・ナビゲーション・ポーズ推定などの各機能を統括し、効率的な搬送を実現します。

### 主な機能

- 協調搬送プロセスの統合管理
- 各機能パッケージとの連携
- 実行のためのLaunchファイル提供

---

### Subscriber
#### 各ロボットの入力（ジョイ、状態など）
- Topic: /collab/joy, /collab/sleep, /collab/wakeup
- Type: sensor_msgs::msg::Joy / std_msgs::msg::Empty

### Publisher
#### 実行速度の指令
- Topic: /collab/run_vel
- Type: geometry_msgs::msg::Twist

#### リフト動作の指令
- Topic: /collab/run_lifter
- Type: std_msgs::msg::String

#### 本Node情報をエラー監視モジュールに追加する
- Topic: /except_handl/node/add
- Type: std_msgs::msg::String

#### エラーを発行する
- Topic: /triorb/error/str/add
- Type: std_msgs::msg::String

#### 警告を発行する
- Topic: /triorb/warn/str/add
- Type: std_msgs::msg::String


## Package: triorb_collab_navi

このパッケージは、複数のAMRによる協調搬送中のナビゲーションを担当します。干渉を避けながら、各ロボットが協調して目的地まで搬送を行えるよう支援します。

### 主な機能

- 経路計画と経路追従
- 衝突回避と速度調整
- 複数ロボット間の同期ナビゲーション

---

### Subscriber
#### 経路追従制御の開始命令
- Topic: /drive/init_path_follow
- Type: std_msgs::msg::Empty

#### 一時停止/再開/停止
- Topic: /drive/pause, /drive/resume, /drive/stop
- Type: std_msgs::msg::Empty

### Publisher
#### 搬送完了通知
- Topic: /collab/drive/finish
- Type: std_msgs::msg::Empty

#### 姿勢共有情報
- Topic: /collab/group_pose
- Type: geometry_msgs::msg::PoseArray

#### 本Node情報をエラー監視モジュールに追加する
- Topic: /except_handl/node/add
- Type: std_msgs::msg::String

#### エラーを発行する
- Topic: /triorb/error/str/add
- Type: std_msgs::msg::String

#### 警告を発行する
- Topic: /triorb/warn/str/add
- Type: std_msgs::msg::String


## Package: triorb_collab_pose

このパッケージは、拡張カルマンフィルターなどのセンサフュージョン技術を用いて、AMR自身および協調搬送中の荷物の中心位置を推定します。

### 主な機能

- AMRの自己位置推定
- 複数ロボットからの情報統合
- 荷物中心位置の推定と共有

---

### Subscriber
#### VSLAMからの姿勢受信
- Topic: `/vslam/robot_pose`
- Type: `triorb_drive_interface::msg::TriorbPos3`

#### 各ロボットの姿勢受信
- Topic: `/bc/collab/robot_pose`
- Type: `triorb_drive_interface::msg::TriorbPos3Stamped`

#### バインド姿勢情報受信
- Topic: `/bc/collab/bind/info`
- Type: `triorb_collaboration_interface::msg::ParentBind`

### Publisher
#### 本Node情報をエラー監視モジュールに追加する
- Topic: `/except_handl/node/add`
- Type: `std_msgs::msg::String`

#### エラーを発行する
- Topic: `/triorb/error/str/add`
- Type: `std_msgs::msg::String`

#### 警告を発行する
- Topic: `/triorb/warn/str/add`
- Type: `std_msgs::msg::String`

#### VSLAMからの姿勢リパブリッシュ
- Topic: `/collab/robot_pose`
- Type: `triorb_drive_interface::msg::TriorbPos3Stamped`

#### 協調グループの姿勢リパブリッシュ
- Topic: `/collab/group_pose`
- Type: `triorb_drive_interface::msg::TriorbPos3Stamped`

### TransformBroadcaster
#### 協調グループの姿勢
- Child Frame ID: `${グループ名}`
- Parent Frame ID: `triorb_map`


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

### Publisher
#### 本Node情報をエラー監視モジュールに追加する
- Topic: /except_handl/node/add
- Type: std_msgs::msg::String

#### エラーを発行する
- Topic: /triorb/error/str/add
- Type: std_msgs::msg::String

#### 警告を発行する
- Topic: /triorb/warn/str/add
- Type: std_msgs::msg::String


