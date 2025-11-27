# triorb_collab_navi

**パス**: `triorb_drive/triorb_collab_navi`  
**説明**: 協調搬送中における複数AMRのナビゲーションを担当するパッケージです。経路計画と移動制御を同期させ、干渉のない搬送を実現します。

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
