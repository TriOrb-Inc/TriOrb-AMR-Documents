# triorb_drive

経路生成・軌道追従・区域マップ・静的TF配信などAMR走行制御の基盤パッケージ群です。

## パッケージ一覧

- [triorb_dead_reckoning](./triorb-dead-reckoning.md) — VSLAM・オドメトリ・IMUを統合し自己位置を推定するデッドレコニングパッケージです。IMUセンサ確認用バイパスログ機能も含みます。
- [triorb_drive_pico](./triorb-drive-pico.md) — ROS2メッセージを用いてモーター制御ECUと通信するためのパッケージ
- [triorb_drive_vector](./triorb-drive-vector.md) — 制御指令値からロボットの進行方向や停止・回転などの状態判定を行う
- [triorb_navigation](./triorb-navigation.md) — 自律移動を行うためのパッケージ
- [triorb_navigation_manager](./triorb-navigation-manager.md) — 
   TriOrb製移動ロボット向けのROS 2ノードで、CSVベースの経路ナビゲーションを制御します。
   通常走行、協調走行、リフター動作、地図切替、イベント処理、状態通知などを統合的に管理し、
   TriOrbのドライブ・SLAMシステムと連携可能です。
  
- [triorb_safe_run_cpp](./triorb-safe-run-cpp.md) — C++ implementation of the TriOrb safe run velocity filter.
- [triorb_snr_mux_driver](./triorb-snr-mux-driver.md) — SNR-MUXボードとシリアル通信し、音声再生状態・発進待ち時間などを ROS 2 トピックへ配信するドライバです。navigate / navigation_manager の停止・一時停止の遅延を音声再生と連動させます。
- [triorb_vslam_tf](./triorb-vslam-tf.md) — SLAMで推定した位置姿勢をTriOrb BASEの位置姿勢へ変換しPublishするためのパッケージ
