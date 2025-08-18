# 協調移動 API Reference v1.2.0 (2025-07-17)

## Package: triorb_drive_collaboration

このパッケージは、複数AMRによる協調搬送タスクを統合的に管理するフレームワークです。リフト・ナビゲーション・ポーズ推定などの各機能を統括し、効率的な搬送を実現します。

### 主な機能

- 協調搬送プロセスの統合管理
- 各機能パッケージとの連携
- 実行のためのLaunchファイル提供

---

### Subscriber
#### コントローラー入力受信
- **Topic:** `/collab/joy`  
- **Type:** `sensor_msgs::msg::Joy`  
- **QoS:** `rclcpp::SensorDataQoS()`  
- **概要:** 協調グループの手動操作用ジョイスティック入力を受信します。

---

#### 各ロボットのバインド姿勢設定
- **Topic:** `/bc/collab/bind/set`  
- **Type:** `triorb_collaboration_interface::msg::ParentBind`  
- **QoS:** `rclcpp::ParametersQoS()`  
- **概要:** 各ロボットに対して指定されたバインド姿勢を受信・適用します。

---

#### 各ロボットのバインド姿勢情報受信
- **Topic:** `/bc/collab/bind/info`  
- **Type:** `triorb_collaboration_interface::msg::ParentBind`  
- **QoS:** `rclcpp::SensorDataQoS()`  
- **概要:** 各ロボットから報告される現在のバインド姿勢情報を受信します。

---

#### 各ロボットの最大速度受信
- **Topic:** `/bc/collab/max_vel`  
- **Type:** `triorb_drive_interface::msg::RobotParams`  
- **QoS:** `rclcpp::SensorDataQoS()`  
- **概要:** 協調グループ内の各ロボットの最大速度制限パラメータを受信します。

---

#### 協調グループへの速度指示受信
- **Topic:** `/bc/collab/run_vel`  
- **Type:** `triorb_drive_interface::msg::TriorbRunVel3Stamped`  
- **QoS:** `rclcpp::SensorDataQoS()`  
- **概要:** 協調グループ向けに上位から与えられた速度指令を受信し、自律動作に反映します。


### Publisher
#### AMR自身への速度指令
- **Topic:** `/drive/run_vel`  
- **Type:** `triorb_drive_interface::msg::TriorbRunVel3`  
- **QoS:** `rclcpp::SensorDataQoS()`  
- **概要:** 自身の移動速度（並進＋回転）を指示します。

---

#### ライフタイム設定
- **Topic:** `/drive/set_life_time`  
- **Type:** `std_msgs::msg::UInt16`  
- **QoS:** `rclcpp::ParametersQoS()`  
- **概要:** ノードの動作ライフタイム（タイムアウト）を設定します。

---

#### トルク制限値設定
- **Topic:** `/set/motor/torque`  
- **Type:** `std_msgs::msg::Float32`  
- **QoS:** `rclcpp::ParametersQoS()`  
- **概要:** モーターの最大トルク制限値を設定します。

---

#### バインド姿勢情報（親）
- **Topic:** `/collab/bind/info`  
- **Type:** `triorb_collaboration_interface::msg::ParentBind`  
- **QoS:** `rclcpp::SensorDataQoS()`  
- **概要:** 自律搬送協調におけるバインド情報を定期送信します。

---

#### バインド情報送信用タイマー
- **周期:** 1000 ms  
- **処理関数:** `DriveCollabNode::callback_info_timer`  
- **概要:** `/collab/bind/info` を周期的に送信するためのタイマーです。

---

#### 協調グループの起動（Wakeup）
- **Topic:** `/collab/wakeup`  
- **Type:** `std_msgs::msg::Empty`  
- **QoS:** `rclcpp::ParametersQoS()`  
- **概要:** 協調搬送グループに対する起動命令を送信します。

---

#### 協調グループの停止（Sleep）
- **Topic:** `/collab/sleep`  
- **Type:** `std_msgs::msg::Empty`  
- **QoS:** `rclcpp::ParametersQoS()`  
- **概要:** 協調搬送グループに対する停止命令を送信します。

---

#### 協調グループの速度指令
- **Topic:** `/collab/run_vel`  
- **Type:** `triorb_drive_interface::msg::TriorbRunVel3Stamped`  
- **QoS:** `rclcpp::SensorDataQoS()`  
- **概要:** 協調搬送グループ全体に対する移動速度を指示します。

---

#### リフター動作指令
- **Topic:** `/collab/run_lifter`  
- **Type:** `std_msgs::msg::String`  
- **QoS:** `rclcpp::ParametersQoS()`  
- **概要:** 協調グループに対してリフターの動作（上下など）を指示します。

---

#### 協調剛体の最大速度
- **Topic:** `/collab/vel_max`  
- **Type:** `triorb_drive_interface::msg::TriorbVel3`  
- **QoS:** `rclcpp::SensorDataQoS()`  
- **概要:** 協調構成体の最大移動速度を外部に通知します。

## Package: triorb_collab_navi

このパッケージは、複数のAMRによる協調搬送中のナビゲーションを担当します。干渉を避けながら、各ロボットが協調して目的地まで搬送を行えるよう支援します。

### 主な機能

- 経路計画と経路追従
- 衝突回避と速度調整
- 複数ロボット間の同期ナビゲーション

---

### VSLAM 地図状態

#### 地図ファイルパスの送信
- **Topic:** `/collab/run_slam/map_file_path`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Publisher  
- **概要:** 自ロボットの地図ファイルパスを協調グループへ通知します。

#### 地図ファイルパスの受信
- **Topic:** `/run_slam/map_file_path`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Subscriber  
- **概要:** 自身の地図ファイルパスを受信し、上記トピックへ再送します。

#### 地図ファイル変更通知の送信
- **Topic:** `/collab/run_slam/map_file_changed`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Publisher  
- **概要:** 地図ファイルの更新通知を協調グループへ送信します。

#### 地図ファイル変更通知の受信
- **Topic:** `/run_slam/map_file_changed`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Subscriber  
- **概要:** 更新通知を受信し、協調トピックへ中継します。

#### 各ロボットの地図ファイルパス受信
- **Topic:** `/bc/collab/run_slam/map_file_path`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Subscriber  
- **概要:** 他ロボットの地図パスを受信します。

#### 各ロボットの地図変更通知受信
- **Topic:** `/bc/collab/run_slam/map_file_changed`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Subscriber  
- **概要:** 他ロボットの地図更新通知を受信します。

---

### ロボット状態・姿勢

#### 各ロボットのステータス受信
- **Topic:** `/bc/collab/robot/status`  
- **Type:** `triorb_static_interface::msg::RobotStatus`  
- **Direction:** Subscriber  
- **概要:** 各ロボットの状態（通信・エラー等）を受信します。

#### 各ロボットの姿勢受信
- **Topic:** `/bc/collab/robot_pose`  
- **Type:** `triorb_drive_interface::msg::TriorbPos3Stamped`  
- **Direction:** Subscriber  
- **概要:** 各ロボットの位置・姿勢情報を受信します。

#### 協調グループの姿勢受信
- **Topic:** `/collab/group_pose`  
- **Type:** `triorb_drive_interface::msg::TriorbPos3Stamped`  
- **Direction:** Subscriber  
- **概要:** 協調体全体の代表姿勢を受信します。

#### 協調グループの最大速度受信
- **Topic:** `/collab/vel_max`  
- **Type:** `triorb_drive_interface::msg::TriorbVel3`  
- **Direction:** Subscriber  
- **概要:** グループ全体における速度上限を受信します。

---

### Waypoint 管理

#### 地点記録リクエスト受信
- **Topic:** `/bc/collab/save_waypoint_hash`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Subscriber  
- **概要:** 地点記録のためのハッシュデータを受信します。

#### 地点記録失敗の通知
- **Topic:** `/collab/save_waypoint_failed`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Publisher  
- **概要:** 地点の保存が失敗した場合の通知です。

#### 地点記録実行指示
- **Topic:** `/drive/save_waypoint`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Publisher  
- **概要:** 実際に地点を保存するための実行指示を送信します。

---

### 自律移動制御

#### SetPos リクエスト受信
- **Topic:** `/bc/collab/request/set_pos`  
- **Type:** `triorb_drive_interface::msg::TriorbSetPos3`  
- **Direction:** Subscriber  
- **概要:** 指定位置への移動を要求されます。

#### SetPos 実行指示（協調グループへ）
- **Topic:** `/collab/drive/set_pos`  
- **Type:** `triorb_drive_interface::msg::TriorbSetPos3`  
- **Direction:** Publisher  
- **概要:** 協調搬送時にグループへ位置指定を共有します。

#### SetPos 実行指示（自身へ）
- **Topic:** `/drive/set_pos`  
- **Type:** `triorb_drive_interface::msg::TriorbSetPos3`  
- **Direction:** Publisher  
- **概要:** 自ノードの制御モジュールへ移動指示を行います。

#### 実行結果受信（通常）
- **Topic:** `/bc/drive/result`  
- **Type:** `triorb_drive_interface::msg::TriorbRunResult`  
- **Direction:** Subscriber  
- **概要:** 単体実行の結果を受信します。

#### 実行結果受信（協調）
- **Topic:** `/bc/collab/drive/result`  
- **Type:** `triorb_drive_interface::msg::TriorbRunResultStamped`  
- **Direction:** Subscriber  
- **概要:** 協調制御での結果を受信します。

#### 協調グループの完了通知
- **Topic:** `/collab/drive/completed`  
- **Type:** `triorb_drive_interface::msg::TriorbRunResultStamped`  
- **Direction:** Publisher  
- **概要:** 結果完了を他ノードと共有します。

---

### 実行状態制御（停止・一時停止・再開）

#### 実行終了通知
- **Topic:** `/drive/finish`, `/collab/drive/finish`  
- **Type:** `std_msgs::msg::Bool`  
- **Direction:** Publisher  
- **概要:** 実行の終了を明示的に通知します。

#### 実行一時停止・再開指示
- **Topic:** `/drive/pause`, `/drive/resume`  
- **Type:** `std_msgs::msg::Empty`  
- **Direction:** Publisher  
- **概要:** 処理を一時停止または再開します。

#### 協調グループからの操作指示受信
- **Topic:**  
  - `/bc/collab/drive/stop`  
  - `/bc/collab/drive/pause`  
  - `/bc/collab/drive/resume`  
- **Type:** `std_msgs::msg::Empty`  
- **Direction:** Subscriber  
- **概要:** グループからの停止／一時停止／再開命令を受信します。

---

### パス追従初期化

#### パス追従初期化の実行
- **Topic:** `/drive/init_path_follow`  
- **Type:** `std_msgs::msg::Empty`  
- **Direction:** Publisher  
- **概要:** 自律移動時のパス追従を初期化します。

#### パス追従初期化の受信
- **Topic:** `/bc/collab/drive/init_path_follow`  
- **Type:** `std_msgs::msg::Empty`  
- **Direction:** Subscriber  
- **概要:** 協調グループからの初期化指令を受信します。

---

### フェールセーフ（通信断処理）

#### 最後の通信検知
- **Topic:** `/bc/collab/last_will`  
- **Type:** `std_msgs::msg::String`  
- **Direction:** Subscriber  
- **概要:** 通信断（Last Will）を受信し、強制停止を実施します。

---

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


