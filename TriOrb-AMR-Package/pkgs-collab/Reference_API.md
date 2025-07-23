# API Reference v1.2.0 (2025-07-17)

## 協調移動パッケージ

### [triorb_collab_lift](./triorb_drive/triorb_collab_lift/README.md)
複数のAMRによる協調リフト制御を提供するパッケージです。複数ロボット間でリフト動作を同期し、安全かつ安定的に荷物を持ち上げることを目的としています。
### [triorb_collab_navi](./triorb_drive/triorb_collab_navi/README.md)
協調搬送中における複数AMRのナビゲーションを担当するパッケージです。経路計画と移動制御を同期させ、干渉のない搬送を実現します。
### [triorb_collab_pose](./triorb_drive/triorb_collab_pose/README.md)
センサフュージョン（拡張カルマンフィルターなど）により、AMR自身と荷物中心の姿勢を推定する協調ポーズ推定パッケージです。
### [triorb_drive_collaboration](./triorb_drive/triorb_drive_collaboration/README.md)
複数AMRによる協調搬送全体を統合的に制御するパッケージです。リフト、ナビゲーション、姿勢推定の各機能を統合し、協調搬送の実現を支援します。
