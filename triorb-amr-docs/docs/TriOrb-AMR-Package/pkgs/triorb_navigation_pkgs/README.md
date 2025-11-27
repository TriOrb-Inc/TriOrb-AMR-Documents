# Package: triorb_navigation_pkgs

# TODO
- keyframe 利用モード
- 牽引モード

## ナビゲーションモジュール概要
- triorb_task_modules: 自律移動の指令受付・実行状態管理の処理モジュール群
- triorb_path_planning_modules: パスプランニングの処理モジュール群
- triorb_controller_modules: 制御指令モジュール群
- triorb_path_controller_interface: パスと制御モジュールの実装忘れ防止用(将来的に制御モジュールのみのinterfaceにする)
- triorb_localization_modules: ナビゲーションで利用する自己位置管理モジュール群
- triorb_navigation_utils: ナビゲージョンに必要な数値計算ライブラリ

## 主なデータフロー

### 自律移動時
triorb_task_modules -> triorb_path_planning_modules -> triorb_controller_modules
                            ↑_triorb_localization_modules

### パスプランニング切替時
triorb_task_modules -> triorb_path_planning_modules

### 制御モード切替時
triorb_task_modules -> triorb_path_planning_modules -> triorb_controller_modules

### マップ切替・自己位置推定ロジック時
triorb_task_modules -> triorb_localization_modules

## Topic一覧
### エラーハンドラ通知
- Topic:(prefix)/except_handl/node/add
- Type:std_msgs/String
- Topic:(prefix)/triorb/error/str/add
- Type:std_msgs/String
- Topic:(prefix)/triorb/warn/str/add
- Type:std_msgs/String

### navigation pkgs 外部モジュール用移動データ[automove task publish]
- Topic:(prefix)/drive/run_pos
- Type:TriorbRunPos3 (Option Stamped)
- Topic:(prefix)/drive/run_vel
- Type:TriorbRunVel3 (Option Stamped)
- Topic:(prefix)/drive/result
- Type:TriorbRunResult/Stamped
- Topic:(prefix)/drive/state
- Type:TriorbRunState
- Topic:(prefix)/run_slam/set/enable_camera
- Type:std_msgs/Int8MultiArray

### navigation pkgs 外部モジュール用移動データ[automove task subscribe]
- Topic:(prefix)/drive/set_pos
- Type:TriorbSetPos3
- Topic:(prefix)/drive/stop
- Type:std_msgs/Empty
- Topic:(prefix)/drive/pause
- Type:std_msgs/Empty
- Topic:(prefix)/drive/finish
- Type:std_msgs/Bool
- Topic:(prefix)/drive/restart
- Type:std_msgs/Empty

### navigation pkgs 外部モジュール用移動データ[controller subscribe]
- Topic:(prefix)/setting/drive/gains
- Type:triorb_drive_interface/DriveGains
- Topic:(prefix)/drive/speed_limit_by_safety_plc
- Type:std_msgs/Float32

### automove task to path planner
- Topic:(prefix)/path_planner/open_loop_start
- Type:std_msgs/Empty
- Topic:(prefix)/path_planner/feedback_pos_start
- Type:std_msgs/Empty
- Topic:(prefix)/path_planner/feedback_vel_start
- Type:std_msgs/Empty
- Topic:(prefix)/path_planner/finish
- Type:std_msgs/Bool

### automove task to controller
- Topic:(prefix)/controller/stop
- Type:std_msgs/Empty
- Topic:(prefix)/controller/set_life_time
- Type:std_msgs/UInt16

### automove task to path planner & controller
- Topic:(prefix)/path_control/set_params
- Type:TriorbSetPos3
- Topic:(prefix)/path_control/update_pose
- Type:std_msgs/String
- Topic:(prefix)/path_control/force_stop
- Type:std_msgs/Empty
- Topic:(prefix)/path_control/reset
- Type:std_msgs/Empty
- Topic:(prefix)/path_control/pause
- Type:std_msgs/Empty

### path planner to automove task
- Topic:(prefix)/path_planner/nav_result
- Type:std_msgs/Int32

### path planner to controller
- Topic:(prefix)/controller/send_command
- Type:geometry_msgs/Vector3
- Topic:(prefix)/controller/feedback_command
- Type:std_msgs/Empty

### controller (旧tx vel)
- Topic:(prefix)/controller/send_motion_command
- Type:geometry_msgs/Vector3

## ノード起動方法
```bash
# session 1 コンポーネントコンテナの立上げ
ros2 run rclcpp_components component_container_mt

# session 2 コンポーネントノードのロード 立上げ例
ros2 component load /ComponentManager triorb_linear_path_planner \
linear_path_planner::LinearPathPlanner --node-name sample
```

## Tests
- パッケージはcolcon build --install-base /install/humble以下にインストール済みが前提
   - pkg直下にbuildフォルダがあるとテストが走査しエラーが起きるため注意
- テストの実行コマンド
  - uncrustifyエラーが出るが、無視してよい。
```bash
colcon test  --packages-select triorb_automove_task --event-handlers console_direct+ 
```

- エラーログのみを確認したい場合の実行例
```bash
ctest --test-dir build/triorb_linear_path_planner -R '^test_linear_path_planner$' -V --output-on-failure
```