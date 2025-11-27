# Agent Spec: triorb_linear_path_planner

## 役割
- AutomoveTask から受け取った `TriorbSetPos3` をもとに「回転 → 並進」を段階的に行う直線移動プランナ。`ControllerInterface` を継承し、共通の停止／再開 API と `NAVIGATE_MODES` ビットフラグを解釈する。
- オープンループで大まかな移動を終えた後にフィードバック制御へ橋渡しする役割を持ち、`AFTER_FEEDBACK` ビットが立っている際は `NAVIGATE_RESULT::PROGRESS` を返して AutomoveTask に制御モード切り替えを促す。
- ロボット座標は `/path_control/update_pose` で送られる JSON（`{"x","y","w","deg","stamp"}`）を直接パースし、`triorb_navigation_utils` の幾何ユーティリティ（`calculate_heading_vector` など）で指令ベクトルを算出する。

## 入出力インターフェース
- Publisher（`linear_path_planner::LinearPathPlanner`）
  - `/control/stop` (`std_msgs::msg::Bool`): 速度フィードバック完了時の停止指令。`feedback_vel_navigation_start_callback` 内で `true` を送る。
  - `/controller/send_command` (`geometry_msgs::msg::Vector3`): オープンループ時の回転／並進ベクトル。`x`,`y` は並進、`z` は角度[deg]。
  - `/controller/feedback_command` (`std_msgs::msg::Empty`): コントローラへフィードバック制御開始を通知。
  - `/path_planner/nav_result` (`std_msgs::msg::Int32`): `NAVIGATE_RESULT` を AutomoveTask へ返す。
  - `/triorb/{error,warn}/str/add`, `/except_handl/node/add`: 例外通知およびユニークノード登録。
- Subscriber
  - `/path_control/set_params` (`triorb_drive_interface::msg::TriorbSetPos3`): 目標姿勢や速度・許容誤差の最新値を受信し `goal_pose_`／`params_` に格納。
  - `/path_control/update_pose` (`std_msgs::msg::String`): 現在姿勢 JSON。受信ごとに `previous_vslam_pose_` ↔ `current_vslam_pose_` を更新し、回転／並進の収束判定に使用。
  - `/path_planner/open_loop_start`, `/path_planner/feedback_pos_start`, `/path_planner/feedback_vel_start` (`std_msgs::msg::Empty`): AutomoveTask からの制御モード起動トリガ。
  - `/path_planner/finish` (`std_msgs::msg::Empty`): フィードバック完了通知用の枠。現状は購読のみで動作未実装。

## ステートマシン（オープンループ）
- `OPEN_LOOP_STEP`  
  | ステップ | 概要 |
  | --- | --- |
  | `RESET_SPEED` | `command=(0,0,0)` を出して次の指令前に速度を殺す。`TRANSLATE_ONLY` 指定時は `ROTATE_INIT` をスキップして `TRANSLATION_INIT` へ。 |
  | `ROTATE_INIT` | `calculate_heading_vector()` で必要角度を計算し、`command.z = vec["deg"]` を publish。推定移動時間 `estimate_motion_time_` を `deg / speed.w + (acc+dec)` で算出。 |
  | `ROTATE_FINISH_DETECT` | TF タイムスタンプ差が推定時間以上かつ回頭変化が ±0.5deg 以内になったら `TRANSLATION_INIT` へ。`ROTATE_ONLY` 指定時はこの時点で成功扱い。 |
  | `TRANSLATION_INIT` | 目標方位への並進ベクトル（`command.x/y`）を publish。移動時間は距離 ÷ √(speed.xy) + (acc+dec)。 |
  | `TRANSLATION_FINISH_DETECT` | TF タイムスタンプ差が推定時間以上で移動量が 1 cm 以下ならオープンループ完了。`AFTER_FEEDBACK` 指定時は `FEEDBACK` ビットを立てて `PROGRESS` を送出しフィードバックへ移行。 |
  | `FINISH` | `is_goal_reached()` で閾値内か確認し、`NAVIGATION_SUCCESS` または `NAVIGATION_FAILED` を publish。 |
  | `FORCE_STOP_STEP` | 初期値。`reset_callback()` で `RESET_SPEED` に戻してから開始する。 |

- `is_goal_reached()` は `params_.setting.{tx,ty,tr}` を閾値とし、`TH_SUCCESS_COUNT` (=3) 回連続で閾値内に入ったときだけ成功判定。フィードバックを使わないモードでは 1 回で成功扱いにすることで遷移を早めている。
- いずれのステップでも `is_active_` フラグで再入を防ぎ、最後に `previous_vslam_pose_ = current_vslam_pose_` へ更新する。

## 制御モード切り替え
- AutomoveTask は `run_setting_params.force` を使ってモードを指定する。代表的な組み合わせ：
  - `NAVIGATE_MODES::AFTER_FEEDBACK`: オープンループで粗移動後、`nav_result = PROGRESS` を publish → AutomoveTask がフィードバックモードのトリガ（`/path_planner/feedback_*_start`）を再度送る。
  - `NAVIGATE_MODES::FEEDBACK`: `feedback_pos_navigation_start_callback` が `is_goal_reached()` をチェックしたうえで `/controller/feedback_command` に空メッセージを送り、プランナ自身は追加ベクトルを生成しない。
  - `NAVIGATE_MODES::VELOCITY_DRIVE`: 速度フィードバック開始時に `/control/stop` (Bool) を併用し、プランナ側で完了判定後に停止信号を入れる。
  - `ROTATE_ONLY` / `TRANSLATE_ONLY`: ステートマシンの分岐により片側のステップをスキップ or 早期成功扱いにする。

## 内部データと補助処理
- `params_`（`TriorbSetPos3`）に目標値・速度上限・ゲイン番号を保持し、`goal_pose_` と `current_vslam_pose_` を `std::map<std::string, double>` で管理。これにより JSON との相互変換を簡略化している。
- `previous_vslam_stamp_` と `estimate_motion_time_` を組み合わせ、入力ポーズが更新されるまで完了判定を遅延させる。FT sensor や VSLAM の更新周波数変動に合わせた安全マージン。
- 例外通知は `this->get_name() + " / <message>"` を統一フォーマットで publish。失敗時（`NAVIGATION_FAILED`）は warn topic にエントリを残す。
- `UNIQUE_NODE` 定義により 500 ms 周期で同一ノード多重起動をチェックし、7 回（約 3.5 s）問題なければ監視タイマーを止める。

## 課題 / TODO
1. **インターフェース未実装**: `pause_callback`, `finish_callback`, `restart_callback`, `force_stop_callback`, `set_drive_gains_callback`, `reset_control_parameters`, `callback_timer` など `ControllerInterface` で宣言しているメソッドの実装が抜けており、現状はリンカエラーや未定義動作の原因になる。旧 `Navigator` (`doc/navigation.cpp.backup`) から該当処理を移植する必要がある。
2. **制御コマンドの意味付け**: `/controller/send_command` の `geometry_msgs::msg::Vector3` は角度を度数で扱っており、コントローラ側と単位を揃える仕様整理が必要。必要なら Stamped 型や別メッセージの導入を検討。
3. **`/path_control/update_pose` の JSON 依存**: 例外時は `JSON parse error` ログのみで AutomoveTask へのフィードバックが無い。共通メッセージ型を作成し、失敗時に `NAVIGATE_RESULT::TRANSFORM_FAILED` 相当を通知できる仕組みが欲しい。
4. **安全系 / 停止処理**: `stop_callback` は空実装のまま。`/drive/stop` 受信時にステートマシンを `FORCE_STOP_STEP` に戻し、`NAVIGATE_RESULT::FORCE_STOP` を publish するなど AutomoveTask と整合する振る舞いが必要。
5. **ゲイン・パラメータの反映**: `drive_gains_sub_` を生成していないため実行時ゲイン更新に対応できていない。PID 系コントローラと整合するため `/setting/drive/gains` の購読や CSV ローディングを実装する。
6. **テスト整備**: 回転／並進の遷移・閾値計算・`AFTER_FEEDBACK` 分岐などを gtest / launch testing で自動化し、VSLAM 更新が停滞した場合のタイムアウト挙動も検証できるようにする。

## 参考
- ソース: `triorb_path_planning_modules/triorb_linear_path_planner/src/linear_path_planner.cpp`, `include/linear_path_planner.hpp`
- 旧実装: `doc/navigation.cpp.backup`（`Navigator::run_move_open_loop`, `Navigator::check_success` など）
- 連携モジュール: `triorb_task_modules/triorb_automove_task`, `triorb_controller_modules/{triorb_pid_pos_controller,triorb_pid_vel_controller}`
