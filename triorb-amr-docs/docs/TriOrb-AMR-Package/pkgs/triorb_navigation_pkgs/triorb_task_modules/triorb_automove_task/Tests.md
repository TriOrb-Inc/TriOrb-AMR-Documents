# Tests: triorb_automove_task

AutomoveTask は複数の I/F（Topic/Service/Action）と多数の下位モジュールをハブ接続しているため、**API ごとのシナリオテスト**＋**異常系フェイルセーフ確認**を組み合わせて検証する。以下は現行実装（`src/automove_task.cpp`）をベースにした推奨テストプラン。

---

## 0. 前提
- ROS 2 Humble 以上
- パッケージはcolcon build --install-base /install/humble以下にインストール済み(pkg直下にbuildフォルダがあるとテストが走査しエラーが起きるため注意)
- colcon test  --packages-select triorb_automove_task --event-handlers console_direct+ を実行して手動テストを開始。
- uncrustifyエラーが出るが、無視してよい。
- `ROS_PREFIX`／`STUB_MODE` など環境変数をテスト毎に明示的にセット。
- Path Planner / Controller 群はスタブでもよいが、`/path_planner/nav_result` を publish できるノードを必ず用意する。
- 例外トピック（`/triorb/error/str/add` 等）は `ros2 topic echo` で常時監視しておく。

---

## 1. コンポーネントテスト（gtest 目標）

| ID | 観点 | 手順 (擬似) | 期待結果 |
|----|------|-------------|----------|
| UT-01 | `handle_set_pos_request()` のバリデーション | テストノードから無効速度（負値/NaN）と有効速度を渡し、戻り値を検証 | 無効入力で false / WARN publish、有効で true (`triorb_task_modules/triorb_automove_task/src/automove_task.cpp:300`) |
| UT-02 | `check_navigation_timeout()` | `run_setting_params_.timeout_ms` を短時間に設定し、`nav_start_time_ms_` を過去に偽装 | 閾値超過で true、通常は false (`src/automove_task.cpp:400`) |
| UT-03 | `update_vslam_pose()` 例外 | `tf_buffer_->lookupTransform` をモックし、空 frame / 同一 stamp を返す | `navigate_result_` が `TRANSFORM_FAILED` / `NO_CHANGE_TIMESTAMP` に遷移 (`src/automove_task.cpp:452-507`) |
| UT-04 | `reset_params()` のリセット通知 | `/path_control/reset` の subscriber を用意し、`handle_set_pos_params()` or `reset_params()` を直接呼ぶ | `/path_control/reset` に `std_msgs::msg::Empty` が publish され、`navigate_stop_order_` 等のフラグがクリアされる (`src/automove_task.cpp:320-347`) |

> gtest 化する場合は `ament_cmake_gtest` を利用し、`tf2_ros::Buffer` を Fake 実装に差し替えるのが現実的。

---

## 2. トピック経由ナビゲーション（MESSAGE）

1. `ros2 run triorb_automove_task automove_task_node --ros-args -p pub_run_pos:=/test/run_pos ...` で起動。  
2. `/drive/set_pos` に `TriorbSetPos3` を publish。  
3. `/path_control/set_params` / `/path_planner/open_loop_start` が送信されることを確認（`src/automove_task.cpp:140-170, 566-580`）。  
4. Path Planner スタブから `/path_planner/nav_result` に `NAVIGATION_SUCCESS`（`std_msgs::msg::Int32`）を送る。  
5. `/drive/result` が success で publish、ライフタイム topic が 0 クリアされることを確認（`src/automove_task.cpp:655-760`）。

### 異常系
- `/drive/stop` 送信 → `/controller/stop` publish と `NAVIGATE_RESULT::FORCE_STOP` になること。  
- TF 未取得状態にすると WARN が出て `TRANSFORM_FAILED` 経由で `/drive/result` が失敗化すること。

---

## 3. Service 経路（SYNC）

| Step | 詳細 |
|------|------|
| 1 | `ros2 service call /srv/drive/set_pos triorb_drive_interface/srv/TriorbSetPos3 "{...}"` を実行。 |
| 2 | コールバック内ループが `navigate_result_` を監視し、`NAVIGATION_SUCCESS` を返すまで待つことを確認（`src/automove_task.cpp:1009-1085`）。 |
| 3 | 実行中に `/drive/pause` → `/drive/restart` を送って PAUSE/RESUME を検証。 |
| 4 | `/drive/stop` を送信すると即座に Service 応答が失敗で返り、ライフタイムが 0 になることを確認。 |

**注意**: Service 実行中に `/drive/set_pos` を送ると `NAVIGATE_RESULT::REJECT` で弾かれるべき (`src/automove_task.cpp:927-957`)。

---

## 4. Action 経路（WAYPOINT）

1. `ros2 action send_goal /action/drive/set_path triorb_drive_interface/action/TriorbSetPath "{path:[...]}"`
2. リクエスト内の全 waypoint が検証され、1 つでも不正なら goal reject → 例外トピックに WARN（`src/automove_task.cpp:969-1007`）。  
3. 受理後は `pop_abs_pos_list()` が順次 `handle_set_pos_params()` を呼び、各 waypoint 達成で `Feedback` が送出される。  
4. Path Planner スタブが waypoint ごとに `NAVIGATION_SUCCESS`/`PROGRESS` を返す挙動をシミュレートし、アクション結果が Success で終わることを確認。  
5. 中途で `GoalHandle.cancel_goal()`（または `ros2 action send_goal ... --cancel-goal-after 3`）を実行し、`navigation_action_cancel()` が ACCEPT を返すかを確認。

---

## 5. 例外処理 / フェイルセーフ

- **ローカライズ喪失**: TF 更新を止めて `LOCALIZE_timeout_count_MAX` が閾値に達した際、WARN・`NAVIGATE_RESULT::LOST_FAILED`・life time reset が揃うか検証。  
- **Timeout**: `run_setting_params_.timeout_ms` を短く設定し、時間切れで `NAVIGATE_RESULT::TIMEOUT_FAILED` → `/controller/stop` が出ること。  
- **Force Success**: `/drive/finish` を `true` で publish → 次の `/drive/stop` が `FORCE_SUCCESS` になること (`src/automove_task.cpp:225-247, 533-565`)。  
- **Unique Node**: 同一ノードを 2 つ起動し、7 回目の `callback_unique_check()` までに片方が強制終了すること (`src/automove_task.cpp:17-64, 1090-1113`)。

---

## 6. STUB_MODE テスト

`STUB_MODE=true` で起動し、`update_vslam_pose()` 内の timestamp ログ抑制や失敗時の WARN が想定通りになるかを確認（`src/automove_task.cpp:48-50, 452-508`）。スタブモードでは TF をモックしやすいため、異常系の自動化に活用する。

---

## 7. 将来の自動化候補

1. **ROS 2 Launch-based integration test**: `launch_testing` を使い、Fake Path Planner/Controller を Python で立ち上げて終端状態を assert。  
2. **Property-based fuzzing**: `handle_set_pos_request()` に対し rapidcheck などで無作為値を入力し、NaN/Inf 伝播が無いか検証。  
3. **Scenario recording**: 実機ログを rosbag2 で記録し、CI でリプレイして `navigation_state` トピックが想定シーケンスになるか比較。

---

## 参考ファイル
- `triorb_task_modules/triorb_automove_task/src/automove_task.cpp`  
- `doc/navigation.cpp.backup`（旧 Navigator の挙動、テストケース抽出に利用）  
- `triorb_task_modules/triorb_automove_task/Agents.md`（I/F 仕様）
