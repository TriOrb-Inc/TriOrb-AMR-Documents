# Agent Spec: triorb_navigation_pkgs

## 概要
- TriOrb プラットフォームの自律移動で利用するナビゲーション系 ROS 2 パッケージ群をまとめたメタパッケージ。
- 上位タスク管理、経路生成、制御ノード、自己位置管理、数値ユーティリティを独立コンポーネントとして提供し、旧 `Navigator` クラスの責務を段階的に分割することが目的。
- 全ノードは `rclcpp_components` でロード可能なコンポーネントとして実装され、例外通知 (`/triorb/{error,warn}/str/add`) やユニークノード監視などの共通ユーティリティを共有する。

## 実行時アーキテクチャとデータフロー
- **標準フロー**: `triorb_task_modules::AutomoveTask` が外部アクション／サービス／トピックから制御指令を受け、適切なパスプランニングノード（例: `triorb_linear_path_planner`）へ目標姿勢をリレー。プランナは制御コマンド（`geometry_msgs::msg::Vector3` など）を生成し、`triorb_controller_modules` の PID ノードに渡して `TriorbRunPos3` / `TriorbRunVel3` 指令を発行する。
- **フィードバック**: `trirob_vslam_tf_bridge` が VSLAM 由来の姿勢をブロードキャストし、タスク／プランナ／コントローラは `/path_control/update_pose` を通じて共通のロボット姿勢を参照。ゴール判定や PID 誤差計算に `triorb_navigation_utils` の関数群を活用する。
- **主要トピック例**（`ROS_PREFIX` により接頭辞が動的付与される）  
  - `/drive/run_pos`, `/drive/run_vel`: AutomoveTask およびコントローラが配信する運動指令  
  - `/controller/feedback_command`: プランナ → コントローラ間のフィードバック制御ハンドシェイク  
  - `/path_planner/nav_result`: プランナからタスクへの到達／失敗通知 (`NAVIGATE_RESULT`)  
  - `/path_control/set_params`, `/setting/drive/gains`: 上位からコントローラへのパラメータ更新チャネル

## モジュール別概要

### triorb_task_modules
- **`triorb_automove_task`**  
  - 自律移動全体の状態機械を管理するコアノード。Action／Service／Topic 起動の三系統をサポートし、ゴール列管理、タイムアウト監視、VSLAM ロスト判定を担当。  
  - 主要 Publisher: `/drive/run_pos`, `/drive/run_vel`, `/drive/run_result`, `/triorb/warn/str/add`, `/path_control/set_params`, `/setting/drive/gains` など。  
  - 主要 Subscriber: `/drive/stop`, `/drive/pause`, `/path_planner/nav_result`, `/controller/feedback_command`, `/path_planner/feedback_*_start` など。  
  - 約 150 ms 周期のタイマーでナビゲーションループを実行し、`triorb_navigation_utils` のゴール判定／PID 初期化を利用して旧 Navigator の制御分岐を再構成している。

### triorb_path_planning_modules
- 旧 Navigator の経路生成ロジックをシナリオごとに分割するパッケージ群。現状は `triorb_linear_path_planner` が主実装で、他プランナはテンプレート状態。
- **`triorb_linear_path_planner`**  
  - 直線移動＋回転を段階的に行うオープンループ制御を提供。`OPEN_LOOP_STEP` ステートマシン（RESET → ROTATE → TRANSLATE → FINISH）を保持し、必要に応じて `/controller/feedback_command` を発火してフィードバック制御へ移行。  
  - `/path_control/set_params` から受け取った `TriorbSetPos3` を `set_params_callback` で保持し、`geometry_msgs::msg::Vector3` 経由で PID コントローラへベクトル指令を送信。`/path_planner/nav_result` で `NAVIGATE_RESULT` を報告し、異常時は `/triorb/warn/str/add` へメッセージを発行。
- **`triorb_follow_path_planner` / `triorb_keyframe_path_planner` / `triorb_towing_path_planner`**  
  - ライセンスチェックやユニークノード監視などのテンプレートのみ実装。旧システムのフォローモード／キーフレームモード／牽引モードの移植予定地として配置。

### triorb_controller_modules
- すべて `triorb_path_controller_interface::ControllerInterface` を実装し、停止・再開・ゲイン更新などの共通 API を提供。
- **`triorb_pid_pos_controller`**  
  - 位置ベース PID コントローラ。`/controller/send_command` で受け取った位置ベクトルをクランプし、`TriorbRunPos3` を `/drive/run_pos` へ publish。積分飽和 (`GAIN_I_XY_SUM_MAX` など) と PLC 安全速度係数による制限を実装。例外時は `/triorb/{error,warn}/str/add` へ通知。  
- **`triorb_pid_vel_controller`**  
  - 速度ベース PID コントローラ。`triorb_navigation_utils::PIDVelocityController` を用いて並進・回転速度を補償し、`/drive/run_vel` / `/drive/run_vel_stamped` を発行。`/drive/set_life_time` で寿命管理、`/setting/drive/gains` でゲイン更新。  
- **`triorb_path_follow_controller`**  
  - 旧フォローモード移植用の骨組み。例外通知やユニークノード検出は実装済みだが、速度生成ロジックは未移植。

### triorb_localization_modules
- **`trirob_vslam_tf_bridge`**  
  - VSLAM 系 TF／キーフレームをナビゲーション系へ橋渡しする予定のブリッジノード。現在はテンプレート状態で、AutomoveTask の `update_vslam_pose` と整合させる処理が今後の課題。

### triorb_navigation_utils
- 角度・距離計算 (`calculate_heading_vector`, `calculate_pose_distance`)、ゴール判定 (`isGoalWithinThreshold`)、PID 補助 (`PIDVelocityController`)、CSV ゲインローダ (`load_gain_csv`, `load_gain_list`) などナビゲーション共通処理を集約したヘッダライブラリ。
- 旧 `Navigator` の数学ユーティリティを移植する受け皿として整理されており、`robot_vel_min/max` などのロボット固有パラメータもここで管理する。

### triorb_path_controller_interface
- コントローラ群が実装すべき純粋仮想インターフェースと、`NAVIGATE_MODES`（フィードバック／回転のみ／並進のみ 等）、`NAVIGATE_RESULT`、`VSLAM_LOCALIZE_STATE` といった共通列挙値を定義。
- `TriorbSetPos3` や `DriveGains` に依存する共通 API を明示することで、タスク／プランナ間での互換性と旧システムとのビットフラグ互換を維持する。

## ビルドとコンポーネント起動
```bash
colcon build --packages-select triorb_navigation_pkgs

# コンポーネントマネージャでノードをロードする例
ros2 run rclcpp_components component_container_mt &
ros2 component load /ComponentManager triorb_linear_path_planner \
  linear_path_planner::LinearPathPlanner --node-name sample
```

## 移行状況と TODO
- `triorb_follow_path_planner`, `triorb_keyframe_path_planner`, `triorb_towing_path_planner`, `triorb_path_follow_controller`, `trirob_vslam_tf_bridge` は移植前のテンプレート。`doc/README.md` に列挙された旧 Navigator 機能を参照しながら段階的にロジックを移植する必要がある。  
- PID コントローラはゲイン CSV 読込や例外通知を実装済みだが、ユニットテスト／シミュレーション検証が未整備。`triorb_navigation_utils::PIDVelocityController` を利用したテストベンチ整備が推奨。  
- AutomoveTask の手動キーフレーム連携（`set_manual_keyframes_*` 系）や JSON ベースの外部連携は旧システム準拠のままなので、新アーキテクチャに合わせた例外処理・再試行ロジックの見直しが必要。

## 参考資料
- `README.md`: パッケージ一覧とデータフロー概要  
- `doc/navigation.cpp.backup`, `doc/navigation.hpp.backup`: 旧 Navigator 実装のバックアップ。各機能の移植元。  
- 各モジュール配下の `Agents.md`（存在するもの）: 個別ノードの詳細仕様・TODO を補足。
