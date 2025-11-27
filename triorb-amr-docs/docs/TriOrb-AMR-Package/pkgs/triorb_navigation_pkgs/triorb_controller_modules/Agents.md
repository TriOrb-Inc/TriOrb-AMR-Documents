# Agent Spec: triorb_controller_modules

## 役割
- TriOrb ナビゲーションスタックにおける制御層ノード群をまとめる ROS 2 メタパッケージ。
- 各ノードは `triorb_path_controller_interface::ControllerInterface` を継承し、停止／再開／ゲイン更新といった共通 API を通じてタスクモジュール (`triorb_automove_task`) やパスプランナと連携する。
- 旧 `Navigator` クラスの制御ロジックを位置指令系と速度指令系に分割し、ユーティリティ（`triorb_navigation_utils`）との責務分離を進める。

## 全体アーキテクチャ
- **入力経路**: `/controller/send_command`（`geometry_msgs::msg::Vector3`）などのモード別トピックからプランナがコマンドを送出。`/path_control/set_params` と `/setting/drive/gains` で目標姿勢・PID ゲインを更新。
- **出力経路**: `/drive/run_pos` または `/drive/run_vel` に `TriorbRunPos3` / `TriorbRunVel3` を publish。PLC 安全リミットやライフタイム制御は同トピック系で共通化。
- **例外通知**: すべてのノードが `/triorb/error/str/add`, `/triorb/warn/str/add` を用いて警告・エラーを報告。ユニークノード監視により多重起動を検出。

## サブモジュール概要
- **`triorb_pid_pos_controller`**  
  - 位置ベース PID 制御。`TriorbRunPos3` を出力し、積分サチュレーション (`GAIN_I_XY_SUM_MAX`, `GAIN_I_W_SUM_MAX`) と PLC 速度上限を適用。フィードバック制御トリガーは `/controller/feedback_command`。  
  - `Agents.md`（モジュール内）に詳細仕様と移植 TODO を記載済み。
- **`triorb_pid_vel_controller`**  
  - 速度ベース PID 制御。`TriorbRunVel3` / `TriorbRunVel3Stamped` を出力し、`PIDVelocityController` を使用して並進・回転速度を補償。ライフタイム (`/drive/set_life_time`) や PLC 速度制限に対応。  
  - モジュール内 `Agents.md` に旧 Navigator からの移植ポイントと実装計画を整理。
- **`triorb_path_follow_controller`**  
  - 旧フォローモード移植のためのプレースホルダ。ノードテンプレートとユニークノード監視のみ実装済みで、速度生成ロジックは今後移植予定。

## 共通インターフェースとユーティリティ
- `triorb_path_controller_interface` が `NAVIGATE_MODES`, `NAVIGATE_RESULT`, `VSLAM_LOCALIZE_STATE` を定義し、コントローラが共通の状態ビットを解釈できるようにする。
- `triorb_navigation_utils` 提供の関数を利用してゲイン CSV を読み込み (`load_gain_list`)、PID 演算や速度制限を共通化。
- PLC 速度制限値は各ノードで `limited_speed_by_safety_plc_` を保持し、AutomoveTask からの通知により更新する。

## 主要トピック（デフォルト。`ROS_PREFIX` で接頭辞変化）
- `/controller/send_command`: プランナ → PID コントローラ（位置／速度共通）  
- `/controller/feedback_command`: プランナがフィードバック制御ループ開始を促すトリガ  
- `/path_control/update_pose`: 自己位置情報（`std_msgs::msg::String` JSON）  
- `/setting/drive/gains`: PID ゲイン更新  
- `/drive/run_pos`, `/drive/run_vel`: 実機ドライバへ送る制御指令  
- `/drive/set_life_time`: 速度制御寿命設定（速度コントローラのみ）

## TODO / 課題
1. `triorb_path_follow_controller` の旧コード移植（速度追従ロジック、`tx_vel_follow` 等）とユニットテスト整備。  
2. PID コントローラ間で重複している PLC 制限処理や例外通知処理を共通ヘルパー化し、`ControllerInterface` へ拡張メソッドとして集約。  
3. `/controller/send_command` の型（位置/速度）を明示するメッセージ設計の再検討。必要に応じて別トピックへ分割。  
4. `triorb_navigation_utils::PIDVelocityController` を利用したシミュレーション・単体テストベンチの作成。  
5. 例外通知メッセージの規約整備（フォーマット・重大度）と、テレメトリ／ログシステムとの連携。

## 参考
- 個別モジュールの `Agents.md`  
- `doc/navigation.cpp.backup` / `doc/navigation.hpp.backup`: 旧 Navigator の制御処理割り当て表  
- `triorb_navigation_pkgs/Agents.md`: ナビゲーション全体のアーキテクチャ概要
