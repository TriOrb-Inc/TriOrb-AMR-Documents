# 協調移動 API Reference v1.2.3 (2025-11-28)

各パッケージのリファレンスをセクションごとに分割した構成です。
サイドバーの階層ナビゲーション、またはこのページの目次から目的のパッケージに移動できます。

## triorb_drive

協調搬送向けの走行・ポジショニング機能を提供するパッケージ群です。

[triorb_drive のパッケージ一覧](./triorb-drive/index.md)

### [triorb_collab_lift](./triorb-drive/triorb-collab-lift.md)

複数のAMRによる協調リフト制御を提供するパッケージです。複数ロボット間でリフト動作を同期し、安全かつ安定的に荷物を持ち上げることを目的としています。

### [triorb_collab_navi](./triorb-drive/triorb-collab-navi.md)

協調搬送中における複数AMRのナビゲーションを担当するパッケージです。経路計画と移動制御を同期させ、干渉のない搬送を実現します。

### [triorb_collab_pose](./triorb-drive/triorb-collab-pose.md)

センサフュージョン（拡張カルマンフィルターなど）により、AMR自身と荷物中心の姿勢を推定する協調ポーズ推定パッケージです。

### [triorb_drive_collaboration](./triorb-drive/triorb-drive-collaboration.md)

複数AMRによる協調搬送全体を統合的に制御するパッケージです。リフト、ナビゲーション、姿勢推定の各機能を統合し、協調搬送の実現を支援します。
