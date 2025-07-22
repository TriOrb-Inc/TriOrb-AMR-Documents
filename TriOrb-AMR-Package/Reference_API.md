# API Reference 1.2.0 (2025-07-17)

## 自律移動パッケージ

### triorb_slam_interface
TODO: Package description
### [triorb_relative_align_marker](./pkgs/triorb_cv/triorb_relative_align_marker/README.md)
TODO: Package description
### path_planning_server
TODO: Package description
### [triorb_dead_reckoning](./pkgs/triorb_drive/triorb_dead_reckoning/README.md)
TODO: Package description
### [triorb_drive_pico](./pkgs/triorb_drive/triorb_drive_pico/README.md)
ROS2メッセージを用いてモーター制御ECUと通信するためのパッケージ
### [triorb_drive_vector](./pkgs/triorb_drive/triorb_drive_vector/README.md)
TODO: Package description
### [triorb_navigation](./pkgs/triorb_drive/triorb_navigation/README.md)
自律移動を行うためのパッケージ
### [triorb_navigation_manager](./pkgs/triorb_drive/triorb_navigation_manager/README.md)
TODO: Package description
### [triorb_relative_alignment](./pkgs/triorb_drive/triorb_relative_alignment/README.md)
TODO: Package description
### [triorb_stub_pico](./pkgs/triorb_drive/triorb_stub_pico/README.md)
ROS2メッセージを用いてモーター制御ECUと通信するための代替パッケージ
### [triorb_vslam_tf](./pkgs/triorb_drive/triorb_vslam_tf/README.md)
SLAMで推定した位置姿勢をTriOrb BASEの位置姿勢へ変換しPublishするためのパッケージ
### [triorb_job_monitor](./pkgs/triorb_fleet/triorb_job_monitor/README.md)
TODO: Package description
### [triorb_job_scheduler](./pkgs/triorb_fleet/triorb_job_scheduler/README.md)
Taskの順序管理及び実行を行うパッケージ
### [triorb_map_share](./pkgs/triorb_fleet/triorb_map_share/README.md)
複数台ロボットでの地図共有のためのパッケージ
### [triorb_rmf_bridge](./pkgs/triorb_fleet/triorb_rmf_bridge/README.md)
OpenRMF用のTopicのGloal⇔Localバイパスを行う
### [triorb_task_library](./pkgs/triorb_fleet/triorb_task_library/README.md)
 タスク名とタスク内容の紐付け管理を行うパッケージ
### [triorb_gpio](./pkgs/triorb_os/triorb_gpio/README.md)
Jetsonに搭載されたGPIOヘッダを制御するパッケージ
### [triorb_host_info](./pkgs/triorb_os/triorb_host_info/README.md)
ホストコンピューター（Jetson）関連の情報を表示するためのパッケージ
### [triorb_os_setting](./pkgs/triorb_os/triorb_os_setting/README.md)
ホストコンピューター（Jetson）の設定のためのパッケージ
### [triorb_camera_capture](./pkgs/triorb_sensor/triorb_camera_capture/README.md)
カメラキャプチャーのためのパッケージ
### [triorb_sls_drive_manager](./pkgs/triorb_sensor/triorb_sls_drive_manager/README.md)
TODO: Package description
### [triorb_streaming_images](./pkgs/triorb_sensor/triorb_streaming_images/README.md)
映像配信のためのパッケージ
### [triorb_except_handl](./pkgs/triorb_service/triorb_except_handl/README.md)
TODO: Package description


## 協調移動パッケージ

### [triorb_collab_lift](./pkgs-collab/triorb_drive/triorb_collab_lift/README.md)
TODO: Package description
### [triorb_collab_navi](./pkgs-collab/triorb_drive/triorb_collab_navi/README.md)
TODO: Package description
### [triorb_collab_pose](./pkgs-collab/triorb_drive/triorb_collab_pose/README.md)
TODO: Package description
### [triorb_drive_collaboration](./pkgs-collab/triorb_drive/triorb_drive_collaboration/README.md)
TODO: Package description


## 更新履歴

### (2025/07/17) Ver 1.0.1 -> 1.2.0

 ## 概要
v1.2.0では、新機能としてロボットコントローラへの電源電圧表示、エラー管理の統一、Visual SLAM用地図のエクスポート機能、経路逸脱防止モード、協調搬送機能などが追加され、接続不良カメラの検知や通信遅延改善、タスク管理の変更などの機能改善も行われた。バグフィックスとしては協調搬送の不具合改善や制御遅延の改善が含まれる。次回アップデートでは自己位置ロスト時のデッドレコニング機能が追加予定。

### 機能追加

- ロボットコントローラへの電源電圧表示追加
- エラー、警告の拡充と統一管理化
- Visual SLAM用3次元地図を2次元へエクスポートする仕組みを追加
- 地点間移動における経路逸脱防止（回転含み線形移動が可能）モード追加
- 経由点通過時間短縮モードの追加
- GPIOのRead・Write機能追加
- Visual SLAM用地図をPCへダウンロード・PCからアップロードする機能追加
- AprilTagを用いた相対位置決め機能の追加
- 有線接続ゲームパッド（HORIパッド）対応追加
- ロボットコントローラへタスク実行タブの追加
- 特徴点抽出マスクをGUIから簡易編集できる機能を追加
- ロボットコントローラーからキーボードによるリモコン制御機能を追加
- Visual SLAM地図読込予定時間表示機能追加
- ロボットN台を用いた協調搬送機能追加

### 機能改善

- 接続不良カメラの検知と可視化
- Jetsonのネットワーク設定機能拡充
- ロボット間（ホスト間）通信をMQTT化することで通信遅延改善
- 特徴点抽出アルゴリズム改善に伴う高速化および照度変化耐性強化
- 遠方特徴点と近傍特徴点が混在する空間における自己位置推定精度改善
- タスク実行管理をJetson内で実施するよう変更（PCと通信切断後も移動継続）
- Visual SLAMの地図固定ポカヨケ機能をロボットコントローラへ追加
- ロボット筐体仕様毎の速度上限適用機能追加
- 協調搬送の設定UI改善

### バグフィックス

- OS内時計ズレに伴う協調搬送の不具合改善
- 制御ECUフリーズ対策
- ROS+WebSocketの通信スタック増大に伴うロボットコントローラの制御遅延改善

### 次回アップデート準備

- Visual SLAMによる自己位置ロスト時のデッドレコニング機能を限定追加
- セーフティーレーザースキャナ制御用API追加

### (2024/11/29) Ver 1.0.0 -> 1.0.1

#### 移動制御
- 自律移動の滑らかさ改善
    - waypoint.csv内のforceフラグが128のとき滑らかな動きとなる(デフォルトを128に変更)
    - forceフラグが1のとき旧来の動きとなる
- 並進移動中の姿勢ふらつき改善
    - 制御ECUプログラムの改善（リモコン操作時も効果あり）

#### VSLAM
- 特定のカメラが電気的に切断された場合にVisual SLAMのカメラ位置が入れ替わる（Leftの位置にRightが表示され得る）不具合を改善
- 地図初期化時の空間広さ制限を緩和（最初に捉えた特徴点が近すぎる、遠すぎる際に地図スケールが合わない問題を改善）

#### GUI
- ランチャーの各ボタンレスポンスを改善
- 壁接近のための地点登録（幅寄せ）を追加
- ロボットコントローラーから保存するwaypoint.csvにVisual SLAMの地図ファイル名を付与
- 地図固定モードのときにマップ（青色キーフレーム）が表示されない仕様を、ブラウザリロードで表示されるよう改善

#### その他
- ソフトウェアアップグレードの仕組み改善
- ROS2 topicの/robot/statusにバッテリー残量推定値を追加
- ドライブレコーダー機能を追加
