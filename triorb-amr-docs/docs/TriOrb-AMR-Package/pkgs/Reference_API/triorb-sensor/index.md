# triorb_sensor

Argusカメラ入出力、キャリブレーション、ゲームパッド、画像ストリーミングなどのI/Oを扱うパッケージ群です。

## パッケージ一覧

- [sick_flexi_soft](./sick-flexi-soft.md) — SICK PLCとEIP通信するためのパッケージ
- [sick_safetyscanners2](./sick-safetyscanners2.md) — ROS2 Driver for the SICK safetyscanners
- [sick_safetyscanners2_interfaces](./sick-safetyscanners2-interfaces.md) — Interfaces for the sick_safetyscanners ros2 driver
- [sick_safetyscanners_base](./sick-safetyscanners-base.md) — Provides an Interface to read the sensor output of a SICK
  Safety Scanner
- [triorb_sick_plc_wrapper](./triorb-sick-plc-wrapper.md) — SICK製PLCとのEtherNet/IPデータ交換を行い、速度ベクトルや安全入出力をROS 2メッセージとPLCアセンブリ間で変換するラッパーノードです。
- [triorb_sls_wrapper](./triorb-sls-wrapper.md) — 
    Convert SICK SLS RawMicroScanData topics into sensor_msgs/PointCloud messages.
  
- [triorb_camera_argus](./triorb-camera-argus.md) — JetsonのArgus API経由で複数カメラ映像を取得し、回転補正やデバイス割当を行って画像トピックとして配信するノードです。
- [triorb_camera_capture](./triorb-camera-capture.md) — カメラキャプチャーのためのパッケージ
- [triorb_gamepad](./triorb-gamepad.md) — ゲームパッド入力を監視し、走行・リフタ・非常停止などのコマンドをROS 2トピックへ出力するテレオペ用ノードです。
- [triorb_sls_drive_manager](./triorb-sls-drive-manager.md) — SICK SLS用ドライバマネージャ
- [triorb_streaming_image_cpp](./triorb-streaming-image-cpp.md) — カメラのImageトピックを購読し、JPEG/WEBP等へ圧縮してMQTTへ送出する軽量ストリーミングノードのC++実装です。
- [triorb_streaming_images](./triorb-streaming-images.md) — 映像配信のためのパッケージ
