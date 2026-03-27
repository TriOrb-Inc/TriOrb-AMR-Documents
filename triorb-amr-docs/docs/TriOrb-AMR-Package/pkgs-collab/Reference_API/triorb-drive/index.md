# triorb_drive

協調搬送向けの走行系パッケージ群で、姿勢推定、ナビゲーション仲介、リフト同期、統合ドライブ制御をまとめています。

## パッケージ一覧

- [triorb_collab_lift](./triorb-collab-lift.md) — 協調グループからのリフター指示を各ロボットに配信し、結果を集約して完了可否を通知する協調リフト制御ノードです。
- [triorb_collab_navi](./triorb-collab-navi.md) — 協調搬送時のナビゲーション仲介ノードで、各ロボットのVSLAM地図状態や姿勢を共有しつつ、ウェイポイント保存・set_pos指令・停止/再開をグループ単位でハンドリングします。
- [triorb_collab_pose](./triorb-collab-pose.md) — 拡張カルマンフィルターとTF平均化で各ロボットのバインド姿勢や協調グループ中心を推定し、TFを配信する協調ポーズ推定パッケージです。
- [triorb_drive_collaboration](./triorb-drive-collaboration.md) — ゲームパッド入力や走行制限を協調グループ全体に配信し、リフト操作・速度指令・緊急停止をまとめて制御する協調搬送向け統合ドライブノードです。
