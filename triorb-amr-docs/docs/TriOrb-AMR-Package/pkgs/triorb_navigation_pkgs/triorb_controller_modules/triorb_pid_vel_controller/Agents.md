# Agent Spec: triorb_pid_vel_controller

## 役割と概要
- TriOrb ナビゲーション系の **速度型 PID 制御ノード**。`triorb_path_controller_interface::ControllerInterface` を実装し、AutomoveTask/PathPlanner から受け取った `TriorbSetPos3` をもとに並進・回転速度コマンド (`TriorbRunVel3/Stamped`) を生成する。
- 旧 Navigator の `tx_vel` 系ロジックを分離した実装で、`triorb_navigation_utils::PIDVelocityController` により XY と Yaw を同時制御する。`NAVIGATE_MODES::VELOCITY_DRIVE` がセットされていない要求は無視することで、位置制御ノードとの責務分割を保つ。
- `ROS_PREFIX` と `UNIQUE_NODE` を活用し、本番環境での多重起動・例外通知 (`/triorb/{warn,error}/str/add`) を統一的に管理する。

## 入出力インターフェース
- **Publisher**
- `/drive/run_vel` or `/drive/run_vel_stamped` (`set_vel_pub_*, use_stamped_type_`): PID計算結果の速度指令。`send_motion_command_callback()`／`brake()` が利用。
- `/drive/set_life_time` (`order_life_time_pub_`): モータ指令の寿命を AutomoveTask 側へ通知。`is_active_` が true のときのみ Stop/Pause/Finish/ForceStop で 0 を publish、`restart_callback()` は保持している `life_time_ms_` を再送して寿命復旧を試みる。
- `/except_handl/node/add`, `/triorb/error/str/add`, `/triorb/warn/str/add`: 例外監視。
- **Subscriber**
  - `/controller/set_life_time`: モータ寿命パラメータを受信し、`order_life_time_pub_` を経由して実機へ反映。
  - `/controller/feedback_command`: フィードバック制御開始トリガ。`feedback_motion_callback()` が現在姿勢とゴールから速度コマンドを再計算。
  - `/controller/send_motion_command`: Path Planner から直接渡される移動量 (`geometry_msgs::msg::Vector3`) を PID に掛けて publish。
  - `/path_control/set_params`: 最新ゴール／速度制限／ゲイン番号を保持し、`NAVIGATE_MODES::VELOCITY_DRIVE` のときだけ `is_active_` を true にする。
  - `/path_control/update_pose`: JSON で送られる現在姿勢を `pose_visual_` に格納。PID 誤差計算の基礎データ。
  - `/setting/drive/gains`: 速度 PID の動的ゲイン切り替え……だが現状は `return;` のみで無効化されており、将来的な拡張ポイント。
  - `/drive/stop`, `/path_control/pause`, `/drive/finish`, `/drive/restart`, `/path_control/reset`, `/path_control/force_stop`: `ControllerInterface` 規約のステート操作に対応。Stop/Finish は寿命 0 を publish するだけでブレーキしない。Pause/ForceStop は寿命 0＋`brake()`、Restart は `life_time_ms_` を再送、Reset は `reset_control_parameters()` を呼ぶ。
  - `/drive/speed_limit_by_safety_plc`: PLC からの速度上限係数。`send_motion_command_callback()` で最終指令をクリップ。

## 制御フロー
1. **パラメータセット (`set_params_callback`)**
   - `TriorbSetPos3` からゴール座標 (`goal_pose_`) と `params_` を更新。
   - `NAVIGATE_MODES::VELOCITY_DRIVE` でなければ `is_active_` を false のまま返し、速度制御に入らない。
   - ゲイン番号 (`setting.gain_no`) が 1 以上なら `PID_GAIN_LIST` から XY/W の PID を再設定。
2. **現在姿勢の追跡 (`update_pose_callback`)**
   - `/path_control/update_pose` の JSON を `pose_visual_` に取り込み、`feedback_motion_callback()` での PID 誤差計算に備える。
3. **速度指令生成 (`send_motion_command_callback`)**
   - Path Planner や `feedback_motion_callback()` から渡される `Vector3` (x,y=並進量, z=deg) を PID コントローラへ入力。
   - 出力速度が設定上限や `robot_vel_max` を超える場合は XY/Z を正規化し、`TRANSLATE_ONLY`／`ROTATE_ONLY` ビットで片側を強制 0 にする。
   - PLC 制限 (`limited_speed_by_safety_plc_`) を超えると全体のXYベクトルをスケーリングダウンする。
   - Publish 後は `is_active_ = false` として再トリガ待ちに戻る。
4. **フィードバック経路 (`feedback_motion_callback`)**
   - `pose_visual_` が更新されている場合にのみ `calculate_heading_vector()` でゴールとの偏差を求め、内部で `send_motion_command_callback()` を再利用する。
   - これにより open-loop から velocity PID へ継続的に移行できる。
5. **ライフタイムと安全動作**
   - Stop/Finish は `is_active_` 時に寿命 0 を publish するのみ（`brake()` はコメントアウト済み）。Pause/ForceStop は寿命 0 を送ったあとに `brake()` でゼロ速度を publish する。
   - `/drive/restart` は `is_active_ == false` のときだけ `life_time_ms_` を再 publish して寿命を復旧。
   - `/path_control/reset` 受信で `reset_control_parameters()` が呼ばれ、`limited_speed_by_safety_plc_ = sqrt(2*target_speed_.xy^2)` の再計算と `life_time_ms_` の `DEFAULT_LIFE_TIME_MS` 初期化、PID 状態の `reset()` を行う。
   - `/controller/set_life_time` で受信した寿命は `life_time_ms_` に保持し、モータ側へ即座に反映する。
   - `UNIQUE_NODE` タイマーが 500 ms 周期で同名ノード多重起動を監視し、8回目までに単体起動が確認できなければエラートピックへ通知して終了。

## 例外処理 / フェイルセーフ
- JSON パース失敗時は `RCLCPP_ERROR` を出すのみで例外を投げないため、Pose 更新が止まってもノードは動き続ける。この場合 PID 誤差がゼロで固定されるため、上位層で TF 喪失を検知する前提。
- `send_motion_command_callback()` の出力を PLC 値や `get_speed_limit_coef()` でクランプし、モータ能力を超える速度を自動的に抑制。
- Stop/Finish は寿命 0 のみに留まり、`brake()` は Pause/ForceStop 時のみ実行される。例外操作後も `is_active_` を見て動作を抑制することで多重ハンドリングを避ける。

## 未対応 / TODO
1. **`set_drive_gains_callback()` の実装**: 現状は `return` で終了しており、DriveGains メッセージを反映できない。CSV 以外の経路でゲイン変更する必要があれば再実装する。
2. **Stop/Finish でのブレーキ**: 寿命 0 のみで速度ゼロ publish を行っていない。実車要件に合わせて `brake()` 呼び出しの復活可否を検討。
3. **Stamped/非Stamped の動的切り替え**: `use_stamped_type_` フラグは存在するがパラメータや CLI からの設定方法が未整理。`declare_parameter("use_stamped", true)` などの導入が必要。
4. **`feedback_motion_callback` の nullptr 生成バグ**: `geometry_msgs::msg::Vector3::SharedPtr command;` に `make_shared` を行わずフィールドへ直接書き込んでいるため、実行時に未定義動作となる。早急に修正する。
5. **単体テスト不足**: PID計算・PLCスロットル・各コールバックのガード条件を網羅する gtest がまだ限定的。`triorb_path_planning_modules/triorb_linear_path_planner/Tests.md` と同スコープのシナリオが望ましい。

## 参考
- 実装: `triorb_controller_modules/triorb_pid_vel_controller/src/pid_vel_controller.cpp`
- インターフェース: `triorb_controller_modules/triorb_pid_vel_controller/include/pid_vel_controller.hpp`
- 旧ロジック: `doc/navigation.cpp.backup`（`tx_vel`, `run_move_vel`, `tx_brake` など）
