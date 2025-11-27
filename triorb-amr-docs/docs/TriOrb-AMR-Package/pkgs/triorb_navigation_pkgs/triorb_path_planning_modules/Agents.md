# Agent Spec: triorb_path_planning_modules

## 役割
- TriOrb 自律移動スタックにおける経路生成ノード群をまとめた ROS 2 パッケージセット。
- 旧 `Navigator` クラス内部でモードごとに混在していた経路生成ロジックを、直線移動・フォローモード・キーフレーム・牽引といった用途別ノードへ分割する。
- 各ノードは `geometry_msgs::msg::Vector3` などの抽象コマンドで `triorb_controller_modules` に制御ベクトルを渡し、`/path_planner/nav_result` で AutomoveTask に進捗を返す。

## 全体アーキテクチャ
- **入力**: `/path_control/set_params`（`TriorbSetPos3`）で AutomoveTask から目標姿勢と制御モードを受信。`/path_control/update_pose` で最新ロボットポーズを JSON 形式で取得。必要に応じて `/triorb/warn/str/add` 等で例外通知。
- **出力**: `/controller/send_command`（位置／速度ベクトル）、`/controller/feedback_command`（フィードバック切り替えトリガ）、`/path_planner/nav_result`（`NAVIGATE_RESULT`）。停止要求は `/control/stop` などを通じて送信。
- **例外処理**: すべてのノードでユニークノード監視、例外通知 publisher を共通実装。`ROS_PREFIX` によりトピック名を動的に切り替え可能。

## サブモジュール概要
- **`triorb_linear_path_planner`**  
  - 現在の主実装。回転→並進の二段階オープンループ制御を提供し、必要に応じてフィードバックモードへ移行。`OPEN_LOOP_STEP` ステートマシンと `NAVIGATE_RESULT` を持ち、`triorb_navigation_utils` の計算関数を多用。  
  - `/controller/send_command` にベクトルを publish、`/path_planner/nav_result` で成功／失敗を通知。`/triorb/warn/str/add` で失敗理由をログ出力。
- **`triorb_follow_path_planner`**  
  - 旧 Navigator の「経路追従」モード移植用プレースホルダ。ノード作成・例外通知枠組みのみ実装済み。速度追従やウェイポイント補間ロジックは未移植。
- **`triorb_keyframe_path_planner`**  
  - キーフレーム連携型プランナの移植先。現在はテンプレート状態で、キーフレーム生成・保存・切替 API の実装が今後の課題。
- **`triorb_towing_path_planner`**  
  - 牽引（トーイング）モード移植用の枠組み。ライセンスチェック／ユニークノード監視のみ。

## 主要トピック（デフォルト値。`ROS_PREFIX` で動的接頭辞）
- `/path_control/set_params`: AutomoveTask → プランナ（目標姿勢・PID パラメータ）  
- `/path_control/update_pose`: Localization → プランナ（JSON 形式のロボット姿勢）  
- `/path_planner/open_loop_start`, `/path_planner/feedback_pos_start`, `/path_planner/feedback_vel_start`: AutomoveTask からの制御モード切替指示  
- `/controller/send_command`: プランナ → コントローラ（ベクトルコマンド）  
- `/controller/feedback_command`: フィードバック制御移行トリガ  
- `/path_planner/nav_result`: プランナ → AutomoveTask（`NAVIGATE_RESULT`）

## TODO / 課題
1. `triorb_follow_path_planner`, `triorb_keyframe_path_planner`, `triorb_towing_path_planner` への旧 Navigator ロジック移植。機能毎に `doc/navigation.cpp.backup` の担当箇所を反映させる。  
2. `/path_control/update_pose` の JSON パース処理を共通化し、例外ハンドリングをユーティリティとして切り出す。  
3. 経路プランニングアルゴリズムの単体テスト／シミュレーションシナリオ整備。特にオープンループ → フィードバック切替の境界条件を検証する。  
4. コマンド出版インターフェースの明確化（位置／速度ベクトルの区別、Stamped 型対応）。必要なら `/controller/send_command_pos` などトピックを分離。  
5. 自己位置ブリッジ (`trirob_vslam_tf_bridge`) との整合性チェック。タイムスタンプ検証やロスト判定の責務を AutomoveTask と擦り合わせ。

## 参考
- `triorb_navigation_pkgs/Agents.md`: ナビゲーション全体のコンテキスト  
- `doc/navigation.cpp.backup`: 旧 Navigator からの機能割り当て表  
- 各モジュール配下の README / ソースコード（`linear_path_planner.cpp` など）
