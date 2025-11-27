# Tests: triorb_pid_pos_controller

PidPosController は位置型 PID を扱うため、**API 単体テスト**・**位置指令シナリオ**・**フェイルセーフ**を組み合わせて検証する。以下は現状実装（`src/pid_pos_controller.cpp`）を前提にしたテスト設計。

---

## 0. 前提
- ROS 2 Humble 以上。`colcon build --packages-select triorb_pid_pos_controller` 済み。
- テスト実行: `colcon test --packages-select triorb_pid_pos_controller --event-handlers console_direct+`
- `ROS_PREFIX=test` を指定し、トピック名衝突を避ける。

---

## 1. 単体テスト (gtest)

| ID | 観点 | 手順 (擬似) | 期待結果 |
|----|------|-------------|----------|
| UT-01 | `set_params_callback()` | `TriorbSetPos3` を publish。`NAVIGATE_MODES::FEEDBACK/ROTATE_ONLY/TRANSLATE_ONLY` 各組み合わせを与える。 | 許可モードのみ `is_active_` true、ゴール座標が deg→rad 変換され `gain_no` に応じて PID が再設定される。 |
| UT-02 | `update_pose_callback()` | 正常 JSON と破損 JSON を送信し、`pose_visual_` 更新と例外処理を確認。 | `is_active_` true のときだけ pose が更新され、破損 JSON は `RCLCPP_ERROR` で落ちない。 |
| UT-03 | `set_drive_gains_callback()` | `is_active_` を切り替えながら `/setting/drive/gains` を送信。 | 実行中は無視、停止中は `pid_gains_` に値が入る。 |
| UT-04 | `send_motion_command_callback()` | `params_.pos.speed`／`limited_speed_by_safety_plc_`／`NAVIGATE_MODES` を操作し、Publish される `TriorbRunPos3` を検証。 | `TRANSLATE_ONLY` で deg=0、`ROTATE_ONLY` で x/y=0、並進速度が PLC 値でクリップされる。 |
| UT-05 | `reset_callback()` | `pid_error_sum_`、`pid_error_pre_`、`limited_speed_by_safety_plc_` に値を入れて `/path_control/reset` を送信。 | `is_active_` true のときだけリセットが走り、非アクティブ時は変化しない。 |
| UT-06 | `feedback_motion_callback()` | `pose_visual_` と `pid_gains_` をセットし、`pid_error_sum_`/`pid_error_pre_` の更新と `send_motion_command_callback()` 呼び出しを確認。 | PID 計算結果の `Vector3` が生成され、`is_active_` false に戻る（`calculate_heading_vector` 依存部はモックで代替可）。 |

> gtest には `PidPosControllerNode` のラッパーを生成し、テスト用 Node で `/drive/run_pos` を subscribe。`spin_until` を使い publish 結果を待機する。

---

## 2. シナリオテスト (単体ノード)

1. `ros2 run triorb_pid_pos_controller pid_pos_controller_node --ros-args -r __ns:=/test` を起動。
2. `/path_control/set_params` に FEEDBACK モードの `TriorbSetPos3` を送る。
3. `/controller/send_motion_command` に移動量を publish。`/drive/run_pos` が期待値(並進＋回転)で publish され `is_active_` が false になるか確認。

### バリエーション
- `/controller/feedback_command` を叩いて PID ループ (`feedback_motion_callback`) が動くか。
- `/drive/speed_limit_by_safety_plc` を下げ、出力が制限されるか。

---

## 3. フェイルセーフ

| ID | 観点 | 手順 | 期待結果 |
|----|------|------|----------|
| FS-01 | 停止/一時停止/完了 | `/drive/stop`, `/path_control/pause`, `/drive/finish` を送信 | `is_active_` true のときだけコールバックが反応し、不要な publish を抑止できることを確認。 |
| FS-02 | 再開/リセット/強制停止 | `/drive/restart`, `/path_control/reset`, `/path_control/force_stop` を送信 | Reset は `pid_error_sum_` クリアと PLC 制限再計算を行い、非アクティブ時は無視される。 |
| FS-03 | Unique Node | 同一ノードを複数起動 | 500 ms 周期の `callback_unique_check()` で重複起動を検知し、ログと例外トピックへ通知する。 |
| FS-04 | JSON 破損 | `/path_control/update_pose` に壊れた JSON を投げ続ける | `update_pose_callback` がエラー出力のみでクラッシュしない。 |

---

## 4. 将来の自動化案
1. **launch_testing**: AutomoveTask + LinearPathPlanner + PidPosController を同時起動し、`/controller/send_motion_command` → `/drive/run_pos` のシーケンスを統合テスト。
2. **PID パラメータスイープ**: さまざまな `gain_no` と `DriveGains` を切り替え、`pid_error_sum_` の飽和や `DIST_XY_MAX` 制限が正しく働くか fuzz テスト。
3. **HIL/シミュレータ**: Gazebo などで位置指令を実モーションに変換し、目標到達誤差を評価。

---

## 参考ファイル
- `triorb_controller_modules/triorb_pid_pos_controller/src/pid_pos_controller.cpp`
- `triorb_controller_modules/triorb_pid_pos_controller/include/pid_pos_controller.hpp`
- `doc/navigation.cpp.backup`（旧 Navigator の位置制御実装）
