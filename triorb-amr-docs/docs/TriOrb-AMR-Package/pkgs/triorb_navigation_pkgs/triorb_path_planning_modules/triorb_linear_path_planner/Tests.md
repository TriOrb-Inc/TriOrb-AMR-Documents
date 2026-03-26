# Tests: triorb_linear_path_planner

`linear_path_planner::LinearPathPlanner` は AutomoveTask と Controller モジュールの間で「回転 → 並進 → フィードバック移行」を司るため、**ステートマシンの分岐** と **トピック I/F** を重点的に検証する。以下は現状実装（`src/linear_path_planner.cpp`）を前提にしたテスト設計の提案。

---

## 0. 前提
- ROS 2 Humble 以上。`colcon build --packages-select triorb_linear_path_planner` 済み。
- `colcon test --packages-select triorb_linear_path_planner --event-handlers console_direct+` で gtest を実行。
- AutomoveTask 側と同様に `ROS_PREFIX=test` を指定するとトピック衝突を避けやすい。
- `triorb_navigation_utils` のヘッダ更新を反映させるため、ヘッダ修正後は `colcon build --packages-select triorb_navigation_utils triorb_linear_path_planner --cmake-target tests` などで再ビルドすること。

---

## 1. コンポーネントテスト（gtest）

| ID | 観点 | 手順 (擬似) | 期待結果 |
|----|------|-------------|----------|
| UT-01 | `set_params_callback()` | `TriorbSetPos3` を publish → ノード内部の `goal_pose_` / `params_` を確認 | 位置・角度が deg→rad へ変換され、設定値が保持される |
| UT-02 | `update_pose_callback()` | JSON 文字列を送信し、`current_vslam_pose_` が更新されるかを確認。異常 JSON も送る | 正常時は値が更新、異常時は `JSON parse error` ログのみで例外が出ない |
| UT-03 | `is_goal_reached()` | `params_.setting.{tx,ty,tr}` を調整し、閾値内/外の組み合わせをテーブル化 | `NAVIGATE_MODES::ROTATE_ONLY` / `TRANSLATE_ONLY` フラグで軸判定がスキップされる |
| UT-04 | `open_loop_navigation_start_callback()` のフェーズ遷移 | `current_vslam_pose_`・`previous_vslam_pose_`・`params_.pos.speed` をモック、複数回呼び出して `OPEN_LOOP_STEP` が `RESET -> ROTATE -> TRANSLATE -> FINISH` へ進むか確認 | `command_pub_` に送られた `geometry_msgs::msg::Vector3` がステップごとに `x/y/z` のみを使い分ける |
| UT-05 | `AFTER_FEEDBACK` 分岐 | `params_.setting.force` に `AFTER_FEEDBACK` を立て、並進完了時の `nav_result` を購読 | `NAVIGATE_RESULT::PROGRESS` が publish され、`current_step_` が `FINISH` へ遷移する |
| UT-06 | フィードバック開始コールバック | `feedback_pos_start_sub_` and `feedback_vel_start_sub_` に対し start メッセージを送信 | 目標到達時に `NAVIGATE_RESULT::NAVIGATION_SUCCESS`、速度版では `/control/stop` (Bool) も publish される |

> gtest では `rclcpp::NodeOptions().use_intra_process_comms(true)` を使ったコンポーネント起動を推奨。`command_pub_` などの Publisher をテスト用 Node で subscribe しアサートする。

---

## 2. トピック連携テスト（単独起動）
1. `ros2 run triorb_linear_path_planner linear_path_planner_node --ros-args -r __ns:=/test` を起動。  
2. `/path_control/set_params` に目標値 (`TriorbSetPos3`) を publish。  
3. `/path_control/update_pose` に現在姿勢 JSON を周期入力し、`/path_planner/open_loop_start` を叩く。  
4. `/controller/send_command` が「回転→並進」の順でベクトルを publish し、予定時間経過後に `/path_planner/nav_result` へ `NAVIGATION_SUCCESS` が出ることを確認。  

### 異常系
- `/path_control/update_pose` を一定時間止め、推定移動時間を満たしても `TRANSLATION_FINISH_DETECT` が成功判定にならない（`is_active_` が false に戻る）ことを確認。
- `NAVIGATE_MODES::ROTATE_ONLY` をセットし、並進指令が出ないまま成功判定へ移行すること。

---

## 3. AutomoveTask との結合テスト

| Step | 詳細 |
|------|------|
| 1 | AutomoveTask と LinearPathPlanner を同一 Launch で起動（Controller はスタブで可）。 |
| 2 | AutomoveTask の `/drive/set_pos` から目標指令を送る。`SET_PARAMS` が LinearPathPlanner に渡り、`/controller/send_command` が発火する。 |
| 3 | Planner の `NAVIGATE_RESULT` を AutomoveTask が受信し、`/drive/result` に成功/失敗が反映されるか確認。 |
| 4 | AutomoveTask から `/drive/stop` を送信し、Planner の `stop_callback()` が `current_step_` を `RESET_SPEED` に戻す（※未実装の場合は TODO として検出）。 |

---

## 4. フェイルセーフ・例外ハンドリング
- **JSON 破損**: `/path_control/update_pose` に壊れた JSON を送信し、`RCLCPP_ERROR` が出るだけでノードが落ちないことを確認。
- **多重起動**: `UNIQUE_NODE` が有効な状態で同名ノードを2つ起動し、500 ms 周期のチェックで片方が例外終了すること。
- **ROTATE/TRANSLATE しきい値**: `params_.setting.tx` を 0 にした場合、`is_goal_reached()` が `NAVIGATE_MODES::UNKNOWN` をセットして AutomoveTask 側で拒否されるか（協調試験）。

---

## 5. 将来の自動化案
1. **launch_testing**: AutomoveTask / LinearPathPlanner / Controller stub を起動し、特定の目標値で `/path_planner/nav_result` と `/drive/result` のシーケンスをアサート。
2. **Gazebo or Stage シミュレーション**: `controller/send_command` の出力を仮想ロボットに適用し、実際の距離・角度の収束を確認。
3. **Property-based test**: `calculate_heading_vector` と `is_goal_reached` に対して無作為な座標を与え、距離/角度計算の不変条件を検証。

---

## 参考ファイル
- `triorb_path_planning_modules/triorb_linear_path_planner/src/linear_path_planner.cpp`
- `triorb_path_planning_modules/triorb_linear_path_planner/include/linear_path_planner.hpp`
- `triorb_navigation_utils/include/triorb_navigation_utils.hpp`（距離計算・ゴール判定）
- `triorb_task_modules/triorb_automove_task/Tests.md`（上位タスクとの連携テスト例）
