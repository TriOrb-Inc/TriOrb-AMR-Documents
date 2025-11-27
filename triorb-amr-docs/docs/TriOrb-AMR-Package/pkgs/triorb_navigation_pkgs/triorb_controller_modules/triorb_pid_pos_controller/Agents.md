# Agent Spec: triorb_pid_pos_controller

## 役割
- 位置制御専用の PID コントローラ。`triorb_path_controller_interface::ControllerInterface` を実装し、AutomoveTask／PathPlanner が与える `TriorbSetPos3` を `TriorbRunPos3` に変換する。
- 旧 Navigator の `tx_pos`／`run_move` ロジックから PID 計算・サチュレーション・PLC 速度制限を分離し、速度型コントローラと対称な実装に整理した。
- `UNIQUE_NODE` と例外トピック (`/triorb/{warn,error}/str/add`) を共通プラットフォームのルールに従って初期化する。

## 入出力インターフェース
- **Publisher**
  - `/drive/run_pos` (`set_pos_pub_`): 位置指令。`send_motion_command_callback()` が `NAVIGATE_MODES` に応じた並進／回転量を publish し、完了後は `is_active_` を false に戻す。
  - `/except_handl/node/add`, `/triorb/error/str/add`, `/triorb/warn/str/add`: 例外通知。
- **Subscriber**
  - `/controller/send_motion_command`: Path Planner から受け取った並進・回転コマンドを位置指令へ変換する。
  - `/controller/feedback_command`: PID フィードバックを 150 ms 周期でトリガし、`pose_visual_` とゲインから補正量を計算。
  - `/path_control/set_params`: ゴール座標と `NAVIGATE_MODES` を保持し、`VELOCITY_DRIVE` が含まれない要求は無視。`gain_no` >0 の場合は CSV から PID を再設定。
  - `/path_control/update_pose`: JSON 形式で送られる現在姿勢。`is_active_` が true のときのみ `pose_visual_` を更新する。
  - `/setting/drive/gains`: 停止中 (`is_active_` false) に限り `pid_gains_` を更新。
  - `/drive/stop`, `/path_control/pause`, `/drive/finish`, `/drive/restart`, `/path_control/reset`, `/path_control/force_stop`: ControllerInterface 規約のステート操作。すべて `is_active_` を見てガードし、Reset 時だけ `reset_control_parameters()` を実行する。

## 制御フロー
1. **リクエスト受付 (`set_params_callback`)**  
   - `goal_pose_` を deg→rad へ変換して保存し、`NAVIGATE_MODES::FEEDBACK` 等が含まれる場合にのみ `is_active_ = true`。  
   - PLC 上限 (`limited_speed_by_safety_plc_`) の初期値は `params_.pos.speed.xy` から算出。
2. **現在姿勢の追跡 (`update_pose_callback`)**  
   - `is_active_` true のときだけ JSON をパースし `pose_visual_` を更新。破損 JSON は `RCLCPP_ERROR` ログのみで継続する。
3. **位置指令生成 (`send_motion_command_callback`)**  
   - 並進／回転のリクエストを `DIST_XY_MAX` / `DIST_W_MAX` でクリップし、`TRANSLATE_ONLY`／`ROTATE_ONLY` ビットで片側を 0 にする。  
   - 並進と回転が同時指定されたときは、移動距離と `acc/dec` から `speed.w` を再計算し時間同期させる。  
   - PLC 制限 (`limited_speed_by_safety_plc_`) を超える場合は xy 速度をスケーリングし、publish 後は `is_active_ = false`。
4. **PID フィードバック (`feedback_motion_callback`)**  
   - `pose_visual_.stamp > 0` のときだけ `calculate_heading_vector()` から誤差を算出し、PID（P/I/D + 積分クランプ）で `Vector3` を生成。  
   - PID 誤差累積は `GAIN_I_XY_SUM_MAX` / `GAIN_I_W_SUM_MAX` で抑制し、直近誤差を `pid_error_pre_` に保存、`send_motion_command_callback()` を再利用。
5. **リセット (`reset_control_parameters`)**  
   - `/path_control/reset` 受信時、`pid_error_sum_`/`pid_error_pre_` をクリアし、PLC 速度上限を `sqrt(2 * speed.xy^2)` に戻す。`is_active_` が false の場合は何もしない。

## 安全・フェイルセーフ
- Stop/Pause/Finish/ForceStop は `is_active_` true のときだけログを出す。実際のブレーキ処理は上位の `send_motion_command_callback()` でゼロ指令を送る設計。
- Reset は active 状態でのみ PID をクリアし、非アクティブ時の外部リセットで状態が書き換わらないようにしている。
- JSON パース失敗や未初期化 pose では `feedback_motion_callback()` が安全にリターンし、無効な PID 出力を publish しない。
- UNIQUE_NODE 監視により複数起動を検知し、8 回以内に例外ノードへ通知して終了する。

## 今後の拡張
1. Stop/Pause/ForceStop 時に `brake()` 相当のゼロ指令を publish するかどうか、運用方針に合わせて追加検討。
2. `limited_speed_by_safety_plc_` を `/drive/speed_limit_by_safety_plc` トピックで外部更新できるよう、Velocity コントローラと同等の I/F を整備。
3. `feedback_motion_callback()` の `geometry_msgs::msg::Vector3::SharedPtr` を `make_shared` で確保する等、メモリアクセスの安全化。
4. Launch/統合テストで AutomoveTask・PathPlanner と組み合わせた長期試験を行い、PID チューニングを継続する。
