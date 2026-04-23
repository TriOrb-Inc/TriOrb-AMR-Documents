# 自律移動 API Reference v1.2.4 (2026-04-20)

各パッケージのリファレンスをセクションごとに分割した構成です。
サイドバーの階層ナビゲーション、またはこのページの目次から目的のパッケージに移動できます。

## stella_vslam_ros

[stella_vslam_ros のパッケージ一覧](./stella-vslam-ros/index.md)

### [stella_vslam_ros](./stella-vslam-ros/stella-vslam-ros.md)

Visual SLAM package

## tagslam_ws

TagSLAMの管理ノードやサンプルを含むタグSLAM用ワークスペースです。

[tagslam_ws のパッケージ一覧](./tagslam-ws/index.md)

### [tagslam](./tagslam-ws/tagslam.md)

software package for fiducial-marker based SLAM

### [triorb_tagslam_manager](./tagslam-ws/triorb-tagslam-manager.md)

TagSLAM用の地図保存・読込・初期化を一括管理し、tagslam系ノードの再起動や状態通知を行う管理ノードです。

## triorb_drive

経路生成・軌道追従・区域マップ・静的TF配信などAMR走行制御の基盤パッケージ群です。

[triorb_drive のパッケージ一覧](./triorb-drive/index.md)

### [triorb_dead_reckoning](./triorb-drive/triorb-dead-reckoning.md)

VSLAM・オドメトリ・IMUを統合し自己位置を推定するデッドレコニングパッケージです。IMUセンサ確認用バイパスログ機能も含みます。

### [triorb_drive_pico](./triorb-drive/triorb-drive-pico.md)

ROS2メッセージを用いてモーター制御ECUと通信するためのパッケージ

### [triorb_drive_vector](./triorb-drive/triorb-drive-vector.md)

制御指令値からロボットの進行方向や停止・回転などの状態判定を行う

### [triorb_navigation](./triorb-drive/triorb-navigation.md)

自律移動を行うためのパッケージ

### [triorb_navigation_manager](./triorb-drive/triorb-navigation-manager.md)


   TriOrb製移動ロボット向けのROS 2ノードで、CSVベースの経路ナビゲーションを制御します。
   通常走行、協調走行、リフター動作、地図切替、イベント処理、状態通知などを統合的に管理し、
   TriOrbのドライブ・SLAMシステムと連携可能です。
  

### [triorb_safe_run_cpp](./triorb-drive/triorb-safe-run-cpp.md)

C++ implementation of the TriOrb safe run velocity filter.

### [triorb_snr_mux_driver](./triorb-drive/triorb-snr-mux-driver.md)

SNR-MUXボードとシリアル通信し、音声再生状態・発進待ち時間などを ROS 2 トピックへ配信するドライバです。navigate / navigation_manager の停止・一時停止の遅延を音声再生と連動させます。

### [triorb_vslam_tf](./triorb-drive/triorb-vslam-tf.md)

SLAMで推定した位置姿勢をTriOrb BASEの位置姿勢へ変換しPublishするためのパッケージ

## triorb_os

Jetson設定・GPIO制御・ネットワークユーティリティ・バッテリー情報収集などOSレイヤの運用支援ツール群です。

[triorb_os のパッケージ一覧](./triorb-os/index.md)

### [triorb_battery_info](./triorb-os/triorb-battery-info.md)

CAN経由で受信したバッテリーSOC・各モジュール電圧/電流を集約し、/battery/status として配信するパッケージです。

### [triorb_gpio](./triorb-os/triorb-gpio.md)

GPIOを通じてAMRの外部デバイス（ランプ・ブザー・トリガ等）を制御するためのノードを提供するパッケージです。

### [triorb_host_info](./triorb-os/triorb-host-info.md)

ホストコンピューター（Jetson）関連の情報を表示するためのパッケージ

### [triorb_socket](./triorb-os/triorb-socket.md)

TCPソケット通信のためのパッケージ

## triorb_sensor

Argusカメラ入出力、キャリブレーション、ゲームパッド、画像ストリーミング、CANブリッジ、SICK製セーフティレーザスキャナ/PLCなどのI/Oを扱うパッケージ群です。

[triorb_sensor のパッケージ一覧](./triorb-sensor/index.md)

### [sick_flexi_soft](./triorb-sensor/sick-flexi-soft.md)

SICK PLCとEIP通信するためのパッケージ

### [sick_safetyscanners2](./triorb-sensor/sick-safetyscanners2.md)

ROS2 Driver for the SICK safetyscanners

### [sick_safetyscanners2_interfaces](./triorb-sensor/sick-safetyscanners2-interfaces.md)

Interfaces for the sick_safetyscanners ros2 driver

### [sick_safetyscanners_base](./triorb-sensor/sick-safetyscanners-base.md)

Provides an Interface to read the sensor output of a SICK
  Safety Scanner

### [triorb_sick_plc_wrapper](./triorb-sensor/triorb-sick-plc-wrapper.md)

SICK製PLCとのEtherNet/IPデータ交換を行い、速度ベクトルや安全入出力をROS 2メッセージとPLCアセンブリ間で変換するラッパーノードです。

### [triorb_sls_wrapper](./triorb-sensor/triorb-sls-wrapper.md)


    Convert SICK SLS RawMicroScanData topics into sensor_msgs/PointCloud messages.
  

### [triorb_camera_argus](./triorb-sensor/triorb-camera-argus.md)

JetsonのArgus API経由で複数カメラ映像を取得し、回転補正やデバイス割当を行って画像トピックとして配信するノードです。

### [triorb_camera_capture](./triorb-sensor/triorb-camera-capture.md)

カメラキャプチャーのためのパッケージ

### [triorb_can](./triorb-sensor/triorb-can.md)

SocketCANを用いてCANバスとROS 2トピック（/can_bridge/rx, /can_bridge/tx）を相互接続するブリッジパッケージです。

### [triorb_gamepad](./triorb-sensor/triorb-gamepad.md)

ゲームパッド入力を監視し、走行・リフタ・非常停止などのコマンドをROS 2トピックへ出力するテレオペ用ノードです。

### [triorb_sls_drive_manager](./triorb-sensor/triorb-sls-drive-manager.md)

SICK SLS用ドライバマネージャ

### [triorb_streaming_image_cpp](./triorb-sensor/triorb-streaming-image-cpp.md)

カメラのImageトピックを購読し、JPEG/WEBP等へ圧縮してMQTTへ送出する軽量ストリーミングノードのC++実装です。

### [triorb_streaming_images](./triorb-sensor/triorb-streaming-images.md)

映像配信のためのパッケージ

## triorb_service

例外処理や共通サービスノードなど、アプリケーション横断の基盤機能を提供します。

[triorb_service のパッケージ一覧](./triorb-service/index.md)

### [triorb_beacon](./triorb-service/triorb-beacon.md)

ホストの IP・プレフィクス情報・グループ情報を定期的に配信

### [triorb_except_handl](./triorb-service/triorb-except-handl.md)

各ノードからの例外・警告を収集し、監視対象ノードの死活チェックや再起動スクリプト実行を行う例外ハンドリングノードです。
