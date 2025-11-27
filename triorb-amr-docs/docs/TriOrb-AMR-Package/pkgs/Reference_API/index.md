# 自律移動 API Reference v1.2.3 (2025-11-28)

各パッケージのリファレンスをセクションごとに分割した構成です。
サイドバーの階層ナビゲーション、またはこのページの目次から目的のパッケージに移動できます。

## stella_vslam_ros

[stella_vslam_ros のパッケージ一覧](./stella-vslam-ros/index.md)

### [stella_vslam_ros](./stella-vslam-ros/stella-vslam-ros.md)

The ROS2 package for stella_vslam

## tagslam_ws

TagSLAMワークスペース関連のサンプルと管理用パッケージ群です。

[tagslam_ws のパッケージ一覧](./tagslam-ws/index.md)

### [triorb_tagslam_manager](./tagslam-ws/triorb-tagslam-manager.md)

TODO: Package description

## triorb_drive

走行制御・ナビゲーション・安全走行に関するパッケージ群です。

[triorb_drive のパッケージ一覧](./triorb-drive/index.md)

### [triorb_dead_reckoning](./triorb-drive/triorb-dead-reckoning.md)

vslam・odometry・imuデータからisam2で位置情報を推定する

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

### [triorb_vslam_tf](./triorb-drive/triorb-vslam-tf.md)

SLAMで推定した位置姿勢をTriOrb BASEの位置姿勢へ変換しPublishするためのパッケージ

## triorb_fleet

RMF連携などフリート運用向けのブリッジパッケージです。

[triorb_fleet のパッケージ一覧](./triorb-fleet/index.md)

### [triorb_rmf_bridge](./triorb-fleet/triorb-rmf-bridge.md)

OpenRMF用のTopicのGloal⇔Localバイパスを行う

## triorb_os

OSレイヤの設定やGPIO・ネットワークユーティリティをまとめています。

[triorb_os のパッケージ一覧](./triorb-os/index.md)

### [triorb_gpio](./triorb-os/triorb-gpio.md)

GPIOを通じてAMRの外部デバイス（ランプ・ブザー・トリガ等）を制御するためのノードを提供するパッケージです。

### [triorb_host_info](./triorb-os/triorb-host-info.md)

ホストコンピューター（Jetson）関連の情報を表示するためのパッケージ

### [triorb_socket](./triorb-os/triorb-socket.md)

TCPソケット通信のためのパッケージ

## triorb_sensor

各種センサー・カメラ入出力やストリーミングを扱うパッケージ群です。

[triorb_sensor のパッケージ一覧](./triorb-sensor/index.md)

### [sick_flexi_soft](./triorb-sensor/sick-flexi-soft.md)

TODO: Package description

### [sick_safetyscanners2](./triorb-sensor/sick-safetyscanners2.md)

ROS2 Driver for the SICK safetyscanners

### [sick_safetyscanners2_interfaces](./triorb-sensor/sick-safetyscanners2-interfaces.md)

Interfaces for the sick_safetyscanners ros2 driver

### [sick_safetyscanners_base](./triorb-sensor/sick-safetyscanners-base.md)

Provides an Interface to read the sensor output of a SICK
  Safety Scanner

### [triorb_sick_plc_wrapper](./triorb-sensor/triorb-sick-plc-wrapper.md)

TODO: Package description

### [triorb_sls_wrapper](./triorb-sensor/triorb-sls-wrapper.md)


    Convert SICK SLS RawMicroScanData topics into sensor_msgs/PointCloud messages.
  

### [triorb_camera_argus](./triorb-sensor/triorb-camera-argus.md)

TODO: Package description

### [triorb_camera_capture](./triorb-sensor/triorb-camera-capture.md)

カメラキャプチャーのためのパッケージ

### [triorb_gamepad](./triorb-sensor/triorb-gamepad.md)

TODO: Package description

### [triorb_sls_drive_manager](./triorb-sensor/triorb-sls-drive-manager.md)

SICK SLS用ドライバマネージャ

### [triorb_streaming_image_cpp](./triorb-sensor/triorb-streaming-image-cpp.md)

TODO: Package description

### [triorb_streaming_images](./triorb-sensor/triorb-streaming-images.md)

映像配信のためのパッケージ

## triorb_service

共通サービスや例外処理など、アプリケーション横断の基盤機能を提供します。

[triorb_service のパッケージ一覧](./triorb-service/index.md)

### [triorb_beacon](./triorb-service/triorb-beacon.md)

ビーコン

### [triorb_except_handl](./triorb-service/triorb-except-handl.md)

TODO: Package description
