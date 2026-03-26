# Tests: triorb_pid_vel_controller

PidVelController は速度 PID の中核なので、**API 単体テスト**＋**速度指令の端点シナリオ**＋**フェイルセーフ確認**を組み合わせる。以下は現行実装 (`src/pid_vel_controller.cpp`) を前提にした推奨テスト設計。

---

## 0. 前提
- ROS 2 Humble 以上。`colcon build --packages-select triorb_pid_vel_controller` 済み。
- テスト実行例: `colcon test --packages-select triorb_pid_vel_controller --event-handlers console_direct+`
- `ROS_PREFIX=test` を指定するとトピック衝突を避けやすい。
- `triorb_navigation_utils` のヘッダ更新がある場合は再ビルド必須。

---

## 1. 単体テスト (gtest 例)

| ID | 観点 | 手順 (擬似) | 期待結果 |
|----|------|-------------|----------|
| UT-01 | `set_params_callback()` | `TriorbSetPos3` を送信し、`params_`／`goal_pose_` が更新されるか確認。`NAVIGATE_MODES::VELOCITY_DRIVE` で `is_active_` true、それ以外は false。 | ゴール座標が deg→rad 変換され、ゲイン番号に応じて `PID_GAIN_LIST` が反映される。 |
| UT-02 | `update_pose_callback()` JSON パース | 正常 JSON で `pose_visual_` 更新、破損 JSON で `RCLCPP_ERROR` が出るだけで落ちないか確認。 | 値が最新に置き換わる／例外を投げずに処理続行。 |
| UT-03 | ライフサイクル系 callbacks | `is_active_` の真偽を切り替えつつ `/drive/stop`, `/path_control/pause`, `/drive/finish`, `/drive/restart`, `/path_control/reset` を呼び出し、寿命 publish や `brake()`/`reset_control_parameters()` の発火条件を確認。 | `is_active_` true で Stop/Finish/Pause/ForceStop/Reset が動作、`is_active_` false で Restart のみ動作。Pause/ForceStop では `brake()` が呼ばれ、Stop/Finish は寿命0のみ。 |
| UT-04 | `reset_control_parameters()` | `target_speed_.xy` や `limited_speed_by_safety_plc_`、`life_time_ms_` に任意値を設定してから Reset を呼び、再計算ロジックを検証。 | `limited_speed_by_safety_plc_ = sqrt(2*target_speed_.xy^2)`、`life_time_ms_ = DEFAULT_LIFE_TIME_MS`、PID が `reset()` される。 |
| UT-05 | `send_motion_command_callback()` の出力 | 代表パターン（通常、ROTATE_ONLY、TRANSLATE_ONLY、PLC 制限超過）を指定し、Publish される `TriorbRunVel3` の `vx/vy/vw` を検証。 | フラグによって片側速度が 0 になる／速度上限に達すると正しくスケーリングされる。 |
| UT-06 | `feedback_motion_callback()` | `pose_visual_` を事前に設定し、`feedback_command_sub_` を叩いて `send_motion_command_callback()` が呼ばれるか確認。 | `is_active_` true & pose有効時のみ指令が生成される。 |

> gtest では `pid_vel_controller::PidVelControllerNode` をそのまま生成し、テスト用 Node で publisher/subscriber を束ねる。必要に応じて `LinearPathPlannerTest` と同様の `spin_until` ヘルパを利用。

---

## 2. 速度指令シナリオテスト

1. ノード単体で起動 (`ros2 run triorb_pid_vel_controller pid_vel_controller_node --ros-args -r __ns:=/test`)。
2. `/path_control/set_params` に `NAVIGATE_MODES::VELOCITY_DRIVE` を含む要求を publish。
3. `/controller/send_motion_command` へ目標移動量 (Vector3) を送信し、`/drive/run_vel` が期待値で publish されるか／`is_active_` が false に戻るかを確認。

### バリエーション
- `TRANSLATE_ONLY`: z 速度が常に 0 になるか。
- `ROTATE_ONLY`: x/y 速度が 0 になるか。
- PLC 制限: `/drive/speed_limit_by_safety_plc` を低い値に設定し、最終出力が上限でクリップされるか。

---

## 3. フェイルセーフ / フロー連携

| ID | 観点 | 手順 | 期待結果 |
|----|------|------|----------|
| FS-01 | 停止/完了/一時停止 | `/drive/stop`, `/path_control/pause`, `/drive/finish` を送信 | Stop/Finish では寿命 0 が publish されるのみ。Pause は寿命 0 ＋ `brake()` によるゼロ速度 publish を確認。 |
| FS-02 | 再開/リセット/強制停止 | `/drive/restart`, `/path_control/reset`, `/path_control/force_stop` を送信 | Restart は `life_time_ms_` を再 publish（`is_active_` false 時のみ）、Reset は `reset_control_parameters()` が呼ばれ PLC 制限/寿命が初期化、ForceStop は `brake()` 実行を確認。 |
| FS-03 | Unique Node | 同一ノード名を2つ起動 | 500 ms 周期の `callback_unique_check()` で1つが `exit(-1)` する |
| FS-04 | JSON 破損 | `/path_control/update_pose` に壊れた JSON を連続送信 | エラーが記録されるだけでノードは落ちない |

---

## 4. 将来の自動化案
1. **launch_testing** で AutomoveTask + LinearPathPlanner + PidVelController を同時起動し、`/path_planner/nav_result`→`/drive/run_vel` のシーケンスを通しで検証。
2. **HIL/シミュレータ**: Gazebo や Stage に接続し、実速度が PID 出力に追従するか確認。
3. **Stress Test**: `/drive/speed_limit_by_safety_plc` を階段状に変化させて、速度クリップが不連続にならないかを確認。

---

## 参考
- `src/pid_vel_controller.cpp`
- `include/pid_vel_controller.hpp`
- 旧実装: `doc/navigation.cpp.backup` (`run_move_vel`, `tx_vel`, `tx_brake`)
