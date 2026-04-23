# TriOrb BASE 開発ガイド v1.2.4 (2026-04-20)

## 製品ドキュメント
- [TriOrb Start-up Guide](https://triorb.notion.site/TriOrb-Start-up-Guide-ver-1-2-2-Rev-2-29bb60b1eaf381e5831ce92f008fa9df)
- [Version 1.0.0からのアップグレード手順](https://app.box.com/shared/static/duvgm7ft3d153x2y8ljcgcrqk6o6fjsy.pdf)
- [Version 1.0.0～1.2.2からのアップグレード手順](https://triorb.notion.site/v-e-r-1-1-1-23bb60b1eaf380858d49ccd2112f0d0b)
- [【B500P100-U-06】TriOrb BASE取扱説明書.pdf](https://app.box.com/shared/static/hlpgcnet2bru1wy5u55dlvvhxgojwsb9.pdf)
- [【BAMR01-05】TriOrbBASE自律移動パッケージ_ユーザーズマニュアル.pdf](https://app.box.com/shared/static/bj8ywg2j4v8wezqwebeu6ve6ek59ee0q.pdf)
### In English
- [【B500P100-U-06】TriOrb BASE Operating Manual.pdf](https://app.box.com/shared/static/y9hivu1vo2vqmhzfv75tv0fesc6g8zxt.pdf)
- [【BAMR01-05】TriOrb BASE Autonomous Navigation Package - User Manual.pdf](https://app.box.com/shared/static/263saiuom9qpl27r9s4g6gwcckkzv4xu.pdf)


## [自律移動API (ROS2)](./TriOrb-AMR-Package/pkgs/Reference_API.md)
- ROS2を用いてTriOrbを動かす場合のTopic等インターフェース仕様
- (非公開) [GitHub / TriOrb-AMR-Package](https://github.com/TriOrb-Inc/TriOrb-AMR-Package)

## [協調移動API (ROS2)](./TriOrb-AMR-Package/pkgs-collab/Reference_API.md)
- ROS2を用いて協調移動を実行する場合のTopic等インターフェース仕様
- (非公開) [GitHub / TriOrb-AMR-Package / pkgs-collab](https://github.com/TriOrb-Inc/TriOrb-AMR-Package/tree/master/pkgs-collab)

## [ROS2 Interface](./TriOrb-AMR-Package/pkgs/TriOrb-ROS2-Types/README_types.md)
- ROS2を用いてTriOrbを動かす場合の通信型仕様
- [GitHub / TriOrb-ROS2-Types](https://github.com/TriOrb-Inc/TriOrb-ROS2-Types)

## [制御ECU通信Library (Python)](./triorb-core/README.md)
- エンドユーザーPCからTriOrb制御ECUに直接指令する際のPythonライブラリ
- [GitHub / triorb-core](https://github.com/TriOrb-Inc/triorb-core)

## [TriOrb AMR 制御用サンプルプログラム](./TriOrb-AMR-Package/sample/README.md)
- TriOrb AMRを上位PCなどから制御するためのサンプルプログラム
- (非公開) [GitHub / TriOrb-AMR-Package / sample](https://github.com/TriOrb-Inc/TriOrb-AMR-Package/tree/master/sample)

## [ロボットAPI (WebAPI)](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/)
- WebAPIを用いてTriOrbを動かす場合のインターフェース仕様
- ※自律移動パッケージ起動後に利用可能

## [変更履歴](./TriOrb-AMR-Package/History.md)

---

APIに関する質問や不具合報告はGitHubの[Issue](https://github.com/TriOrb-Inc/TriOrb-AMR-Documents/issues)または[Discussions](https://github.com/TriOrb-Inc/TriOrb-AMR-Documents/discussions)を利用してください。

個人情報、機密情報または非公開での連絡を希望する場合は、公開投稿ではなく `info@triorb.co.jp` を利用してください。GitHub の Issue / Discussions は公開チャネルであり、投稿者 ID を含め匿名性は限定的です。

## Appendix
- [TriOrb markers generator](https://triorb-inc.github.io/TriOrb_Marker_Generator/)
    - [特徴点補助シート生成の設定例](https://triorb-inc.github.io/TriOrb_Marker_Generator/?width=210&height=297&polygons=50)
    - [マーカーシート生成の設定例](https://triorb-inc.github.io/TriOrb_Marker_Generator/?dict=april_36h11&size=100&id=0&num=2&width=210&height=297&polygons=0&marker-layout=v-stack)
