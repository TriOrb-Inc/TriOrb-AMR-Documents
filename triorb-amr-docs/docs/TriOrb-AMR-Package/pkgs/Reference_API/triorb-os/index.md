# triorb_os

Jetson設定・GPIO制御・ネットワークユーティリティ・バッテリー情報収集などOSレイヤの運用支援ツール群です。

## パッケージ一覧

- [triorb_battery_info](./triorb-battery-info.md) — CAN経由で受信したバッテリーSOC・各モジュール電圧/電流を集約し、/battery/status として配信するパッケージです。
- [triorb_gpio](./triorb-gpio.md) — GPIOを通じてAMRの外部デバイス（ランプ・ブザー・トリガ等）を制御するためのノードを提供するパッケージです。
- [triorb_host_info](./triorb-host-info.md) — ホストコンピューター（Jetson）関連の情報を表示するためのパッケージ
- [triorb_socket](./triorb-socket.md) — TCPソケット通信のためのパッケージ
