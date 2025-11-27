# triorb_drive_collaboration

**パス**: `triorb_drive/triorb_drive_collaboration`  
**説明**: 複数AMRによる協調搬送全体を統合的に制御するパッケージです。リフト、ナビゲーション、姿勢推定の各機能を統合し、協調搬送の実現を支援します。

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
