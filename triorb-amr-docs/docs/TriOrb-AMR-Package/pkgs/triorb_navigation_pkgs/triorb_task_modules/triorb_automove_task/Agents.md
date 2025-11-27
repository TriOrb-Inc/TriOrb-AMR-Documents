# Agent Spec: triorb_automove_task

## 役割
- 高レベル移動要求（Topic/Service/Action）を受け付け、適切な Path Planner / Controller モジュールへ処理をファンアウトするタスク層ノード。`ROS_PREFIX` ベースでノード／トピック名を動的に付与できるよう `GET_NODE_NAME` / `GET_TOPIC_NAME` マクロを備える（`include/automove_task.hpp`）。  
- 旧 `Navigator` が一枚岩で担っていた「要求引き受け」「自己位置管理」「プランナ／制御ノード起動」「結果集約」を分離されたモジュール群のハブとして再実装することを目的にしている。  
- 例外通知（`/triorb/error/str/add` など）とユニークノード監視（`UNIQUE_NODE`）を介し、フィールド運用時の多重起動や失敗検知を集中管理する。`STUB_MODE` を環境変数で切り替え、シミュレーションや診断用途でローカライズを擬似化できる。

## ノードライフサイクルと状態管理
- 主要ステートは `NAVIGATE_TRIGGER`（要求経路）、`NAVIGATE_STATE`（UIに通知する進行状態）、`GOAL_CHECK_STATE`（内部ゴール判定）の 3 つ。いずれも `triorb_path_controller_interface::*` の列挙値を再利用することで下位層と整合した状態遷移を実現する（`include/automove_task.hpp`）。  
- ノード起動時に `nav_timer_`（150 ms）と `nav_state_timer_`（1 s）を登録し、前者でナビゲーションループ、後者で `/drive/state` を配信する（`src/automove_task.cpp` 冒頭）。`UNIQUE_NODE` が定義されているため、実行時に 500 ms 周期で同名ノードの重複起動を監視する。  
- ローカライズ喪失判定は `LOCALIZE_timeout_count_MAX`/`*_FIX_KEYFRAME` パラメータで構成され、Transform 取得に失敗した際は WARN を発行し `VSLAM_LOCALIZE_STATE` を `NAVIGATE_RESULT` へ変換する（`src/automove_task.cpp` 内 `update_vslam_pose()`）。  
- `navigation_state_timer_callback()` はゴール到達後の離脱を `TH_LEAVE_GOAL_COUNT` 回で検出し、`NAVIGATE_STATE::LEAVE_GOAL` を通知することで UI に再誘導を促せる。

## 入出力インターフェース
### Publisher
- `/drive/run_pos`, `/drive/run_vel`, `/drive/result`: 旧 Navigator 互換の結果／指令を保持するが、現状は主に Path Planner/Controller 連携にフォーカスしており下位ドライバへの直接出力は未使用。（`src/automove_task.cpp` L80-L117）  
- `/path_planner/open_loop_start`, `/path_planner/feedback_pos_start`, `/path_planner/feedback_vel_start`, `/path_planner/finish`: 実行する制御モードを各プランナへ伝えるトリガ。`NAVIGATE_MODES` の組み合わせによって `navigate()` 内で選択される（L119-L138, L566-L586）。  
- `/path_control/set_params`, `/path_control/update_pose`, `/path_control/force_stop`, `/path_control/reset`: コントローラ／プランナ双方が読む共通パラメータ・姿勢・停止メッセージ。`handle_set_pos_params()` でリクエスト値を publish、`update_vslam_pose()` が JSON 化した現在姿勢を push、`reset_params()` が次ジョブ開始時に `/path_control/reset` を送って両モジュールへリセット指示する（L140-L170, L503-L508, L320-L347）。  
- `/controller/stop`, `/path_control/pause`, `/controller/set_life_time`: Controller Modules のライフサイクル管理。Message/Service 経路で失敗または完了した際にライフタイムを 0 に戻すほか、Pause 系だけは Path Control 名前空間に統一した（L156-L170, L715-L717 など）。  
- `/drive/state`: 進行状況と速度上限を `TriorbRunState` で提示（L589-L643）。  
- `/triorb/error/str/add`, `/triorb/warn/str/add`, `/except_handl/node/add`: 全タスクノードで共通の例外通知経路。起動時に `[instant]<node>` を登録し、以降は WARN/ERROR を逐次 publish（L21-L43）。

### Subscriber / Timer
- `/drive/stop`, `/drive/pause`, `/drive/finish`, `/drive/restart`: 運用中のユーザ操作を受け付け、`navigate_stop_order_` や `GOAL_CHECK_STATE` を切り替える（L185-L207, L212-L248）。  
- `/path_planner/nav_result`: Path Planner から進行ステータスを受け取り `navigate_result_` を同期（L209-L214, L441-L449）。  
- `/drive/set_pos`: メッセージ経由の単発移動要求（L218-L224, L927-L957）。  
- TF `/triorb_map -> robot`: `tf2_ros::Buffer` と `tf_listener_` で常時取得し `current_vslam_pose_` を更新（L62-L65, L452-L508）。  
- Timers: `nav_timer_` は `navigation_timer_callback()` で Message/Action 経由の非同期進行を確認、`nav_state_timer_` はステート発信専用。

### Service / Action
- `/srv/drive/set_pos` (`triorb_drive_interface::srv::TriorbSetPos3`): 長時間ブロッキングとなるため専用コールバックグループを使用し、サービス内部で `navigate()` の while ループを実行する。`navigate_pause_order_` を監視して外部からの stop/pause を反映（L209-L214, L1009-L1085）。  
- `/action/drive/set_path` (`triorb_drive_interface::action::TriorbSetPath`): 受信時にすべてのウェイポイントを `handle_set_pos_request()` で検証し、1 つでも不正なら即 Reject。妥当性確認後に `path_list` へまとめて格納し OLD Navigator 同様 `pop_abs_pos_list()` による逐次実行へ移行する（L969-L1007, L820-L919）。Action フィードバックは `navigate_action_goal_handle_->publish_feedback()` から直接返却。

## 制御フロー
1. **リクエスト受付**: `handle_set_pos_request()` が並進・回転速度や閾値の妥当性を確認し、走行中は `NAVIGATE_RESULT::REJECT` を返す（L300-L339）。  
2. **目標値セット**: `handle_set_pos_params()` が `goal_pose_` と `run_setting_params_` を更新、`/path_control/set_params` へブロードキャストしたあと `reset_params()` で内部ステートと `/path_control/reset` を初期化指示として発行（L340-L422）。  
3. **ローカライズ更新**: `navigate()` 冒頭で `check_navigation_timeout()` ⇒ `update_vslam_pose()` を順に呼び、タイムアウト・Transform 取得失敗・Timestamp 停滞を `NAVIGATE_RESULT` にマップ。成功時は `/path_control/update_pose` に JSON を publish（L513-L586, L452-L508）。  
4. **プランナ／コントローラ着火**: `run_setting_params_.force` の各ビットを解釈し、オープンループ／フィードバック（位置 or 速度）いずれかのトピックを起動。`/path_control/force_stop` は `/drive/stop` 受信時に送信される（L526-L586, L501-L508）。  
5. **進捗集約**: `navigation_timer_callback()` / Service ループが `navigate_result_` に応じて `/drive/result`、Action Result、`/controller/set_life_time` を更新。`NAVIGATE_STATE::FAILED/SUCCESS` だけでなく `FORCE_STOP` や `FORCE_SUCCESS` に応じた WARN/INFO も例外トピックへ流す（L655-L924, L1040-L1085）。  
6. **ゴール後監視**: 1 s 周期の `navigation_state_timer_callback()` で閾値逸脱をカウントし、しきい値超過で `NAVIGATE_STATE::LEAVE_GOAL` に遷移、UI へ再アラートを送る（L589-L643）。

## フィードバックとセーフティ
- `/drive/stop`／`/drive/pause` 経路は `navigate_stop_order_`／`navigate_pause_order_` を介して Service ループにも伝搬するため、同一ノード内で競合が起きない。停止時は必ず `/controller/stop` と寿命 0 を publish。  
- `force_success_` は `/drive/finish` で設定され、次の stop イベントを成功扱いに書き換える仕掛け（L231-L248, L533-L565）。  
- ローカライズ喪失や TF 欠落時は WARN を出しつつ `NAVIGATE_RESULT` を `TRANSFORM_FAILED` 等に更新、結果メッセージにもそのまま格納する。  
- 例外通知は一貫して `this->get_name() + " / <message>"` 形式に整形されているため、ログ収集側でモジュール別フィルタがしやすい。

## 未実装 / 課題メモ
1. **Keyframe / Camera 出力**: `set_manual_keyframes_pub_` と `camera_select_pub_` の Publisher がコンストラクタ内で生成されていないため、`set_abs_pos_callback()` が null 参照で落ちるリスクがある（L929-L955）。トピック仕様（名称・QoS）を決めたうえで初期化する必要がある。  
2. **`create_manual_keyframes_msg_from_waypoint` 未移植**: 旧 `Navigator` には実装（`doc/navigation.cpp.backup`）があるものの、本モジュールでは宣言のみ。キーフレーム固定ナビを導入するなら移植が必要。  
3. **`/drive/run_pos`/`/drive/run_vel` の用途再定義**: 現状 publish するだけで誰も購読しておらず、Controller Modules と役割が重複している。直接ドライバ制御を担わないなら整理したい。  
4. **Service ループのスピン**: `/srv/drive/set_pos` は `rclcpp::sleep_for()` ベースの busy loop のままであり、`state_pub_time` など未使用変数も残る。将来的に Action 専用に集約する判断も検討が必要。

## 参考リソース
- `triorb_task_modules/triorb_automove_task/include/automove_task.hpp`: インターフェース宣言、状態列挙、メンバ構成。  
- `triorb_task_modules/triorb_automove_task/src/automove_task.cpp`: 具体的なロジックとトピック初期化。  
- `doc/navigation.cpp.backup`: 旧 Navigator 実装。未移植メソッド（Keyframe 関連や PID ヘルパー）の参照元。
