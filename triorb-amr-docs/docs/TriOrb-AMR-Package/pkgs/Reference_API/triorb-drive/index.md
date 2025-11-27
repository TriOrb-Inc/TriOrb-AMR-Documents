# triorb_drive

走行制御・ナビゲーション・安全走行に関するパッケージ群です。

## パッケージ一覧

- [triorb_dead_reckoning](./triorb-dead-reckoning.md) — vslam・odometry・imuデータからisam2で位置情報を推定する
- [triorb_drive_pico](./triorb-drive-pico.md) — ROS2メッセージを用いてモーター制御ECUと通信するためのパッケージ
- [triorb_drive_vector](./triorb-drive-vector.md) — 制御指令値からロボットの進行方向や停止・回転などの状態判定を行う
- [triorb_navigation](./triorb-navigation.md) — 自律移動を行うためのパッケージ
- [triorb_navigation_manager](./triorb-navigation-manager.md) — 
   TriOrb製移動ロボット向けのROS 2ノードで、CSVベースの経路ナビゲーションを制御します。
   通常走行、協調走行、リフター動作、地図切替、イベント処理、状態通知などを統合的に管理し、
   TriOrbのドライブ・SLAMシステムと連携可能です。
  
- [triorb_safe_run_cpp](./triorb-safe-run-cpp.md) — C++ implementation of the TriOrb safe run velocity filter.
- [triorb_vslam_tf](./triorb-vslam-tf.md) — SLAMで推定した位置姿勢をTriOrb BASEの位置姿勢へ変換しPublishするためのパッケージ
