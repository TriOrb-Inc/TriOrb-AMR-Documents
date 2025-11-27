# 自律移動 API Reference v1.2.3 (2025-07-17)

## Package: triorb_gpio

このパッケージは、AMRに搭載されたGPIOインターフェースを通じて、外部デバイス（例：ランプ、ブザー、リレーなど）を制御するノードを提供します。

### 主な機能

- 外部信号出力（ブザー、警告灯）
- GPIOトリガによる動作制御
- エラー通知とログ

### 利用可能なGPIOピン
```
7,11,12,13,15,16,18,22,29,31,32,33,35,36,37,38,40
```

### 設定の保存
GPIOの入出力モード設定は、`/params/gpio.yaml`ファイルに保存されます。出力ピンのHi/Lo状態は保存されません。

---

### Subscriber
#### GPIOの入出力モード設定（複数）
- Topic: /gpios/set_direction
- Type: std_msgs/msg/Int8MultiArray
- Values: -2: NotSet, -1: None, 0: Output, 1: Input
- Usage: 
```bash
## pin 37を非管理、pin 38を入力、pin 40を出力、その他は変更なしに設定
root@agx-orin-XXXX:/ws# ros2 topic pub -1 /gpios/set_direction std_msgs/msg/Int8MultiArray 'data: [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-1,1,0]'
```

#### GPIOの出力値設定（複数）
- Topic: /gpios/set_value
- Type: std_msgs/msg/Int8MultiArray
- Values: -2: NotSet, -1: NotSet, 0: Low, 1: High
- Usage:
```bash
## pin 40をHighに、その他は変更なし
root@agx-orin-XXXX:/ws# ros2 topic pub -1 /gpios/set_value std_msgs/msg/Int8MultiArray 'data: [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-1,-1,1]'
```

#### Publisher
#### GPIOのHi/Lo値（複数）
- Topic: /gpios/value
- Type: std_msgs/msg/Int8MultiArray
- Values: -1: None, 0: Low, 1: High
- Frequency: 1Hz + エッジトリガ

## Package: triorb_host_info

### ホストコンピュータのシステムモニター
Topic：(prefix)/host/status
Type：triorb_static_interface/msg/HostStatus
Frequency：1/1.0 Hz
Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic echo --once /host/status
header:
  stamp:
    sec: 1753410530
    nanosec: 830279666
  frame_id: host_device
memory_percent: 39.599998474121094
cpu_percent: 86.9000015258789
host_temperature: 70.81199645996094
wlan_ssid: TriOrb-WiFi
wlan_signal: 58
wlan_freq: 5180
ping: 10.668999671936035
gateway:
- 192
- 168
- 25
- 1
---
```


## Package: triorb_sls_drive_manager

### Description
- SLS(sick社製)のサンプルモジュール

### install & setup
- Ethernet通信 : サービスとして登録
- 進行方向の取得 : triorb_drive_vector
```bash
sudo bash ./setup.bash
```

### Subscriber
#### ロボットへの絶対位置指示を受信
- Topic: (prefix)/drive/set_pos
- Type: triorb_drive_interface/msg/TriorbSetPos3

#### 推定された運転ベクトル（進行方向・速度など）を受信
- Topic: (prefix)/drive/std_vector
- Type: std_msgs/msg/Float32MultiArray
- Usage: 進行方向のSLSのセンシング範囲を判断する為

#### ロボット状態を受信（励磁やステータス等）
- Topic: (prefix)/robot/status
- Type: triorb_static_interface/msg/RobotStatus

### Publisher
#### 一時停止指示(障害物検知)
- Topic: /drive/pause
- Type: std_msgs/msg/Empty

#### 障害物消失時に自律走行再開指示を出す
- Topic: /drive/wakeup
- Type: std_msgs/msg/Empty

#### 再始動指示
- Topic: /drive/restart
- Type: std_msgs/msg/Empty

#### 速度制限
- Topic: /drive/speed_limit_by_safety_plc
- Type: std_msgs/msg/Float32

#### ノードの動作開始通知
- Topic: (prefix)/_{ノード名}
- Type: std_msgs/msg/Empty

### Service
#### ノードのバージョン情報を取得
- Topic: (prefix)/get/version/{ノード名}
- Type: triorb_static_interface/srv/Version

### Action
本パッケージではActionは利用していません。


## Package: triorb_camera_capture
カメラ映像をキャプチャし, Image型のtopicとしてpublishするためのパッケージ. 

### 主な機能
- ioctlによるカメラ映像の取得
- 画像の平均輝度が一定範囲に収まるように露光・ゲインの調整

### 更新履歴
#### 1.2.0
- カメラ状態を通知するtopic追加
- エラー・ワーニング履歴の通知部分を追加
- 起動時にUSBカメラが1つでも存在していない場合, プログラムが停止するバグ修正

#### 1.1.0
- 画像のENQUEUEをtimer_callbackの最後に全カメラ同時に行うように変更
- gainを設定可能
- gain, exposureを設定時にauto_exposureをオフにするように変更

### camera_capture API
#### カメラ画像受信
- Topic：(prefix)/camera(0-N) # 末尾の整数はカメラのID
- Node：(prefix)_camera_capture
- Type：sensor_msgs/Image
- Frequency：最大1/0.02 Hz
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic info /camera0; ros2 topic hz /camera0
Type: sensor_msgs/msg/Image
Publisher count: 1
Subscription count: 0
average rate: 9.537
        min: 0.072s max: 0.240s std dev: 0.04572s window: 13
...
average rate: 10.766
        min: 0.064s max: 0.240s std dev: 0.02494s window: 266
```

#### カメラ情報受信
- Topic：(prefix)/camera(0-N)_device # 末尾の整数はカメラのID
- Node：(prefix)_camera_capture
- Type：triorb_sensor_interface/msg/CameraDevice
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic echo /camera0_device
header:
  stamp:
    sec: 1753408673
    nanosec: 447031540
  frame_id: cam0
device: /dev/video-csi0
topic: /camera0
id: cam0
state: sleep
rotation: 0
exposure: 0
gamma: 0.0
timer: 0.30000001192092896
```


#### カメラデバイス一覧取得
- Topic：(prefix)/get/camera/state
- Node：(prefix)_camera_capture
- Type：triorb_sensor_interface/srv/CameraDevice
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 service call /get/camera/state triorb_sensor_interface/srv/CameraDevice
...
response:
triorb_sensor_interface.srv.CameraDevice_Response(result=[triorb_sensor_interface.msg.CameraDevice(device='/dev/video0', topic='/camera0', id='cam0', state='awake', rotation=0, exposure=800, gamma=1.0, timer=0.02), ...])
```

#### カメラデバイスの起動・終了
- Topic：(prefix)/set/camera/state
- Node：(prefix)_camera_capture
- Type：triorb_sensor_interface/srv/CameraCapture
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 service call /set/camera/state triorb_sensor_interface/srv/CameraCapture '{request: [{device: /dev/video0, topic: /camera0, id: camera0, state: wakeup, rotation: 0, exposure: 500, gamma: 1.0, timer: 0.1}, {device: /dev/video2, topic: /camera1, id: camera1, state: wakeup, rotation: 0, exposure: 500, gamma: 1.0, timer: 0.1}]}'
...
response:
triorb_sensor_interface.srv.CameraCamture_Response(result=['success','success'])
```

### camera format
- width  1600
- height 1300
- pixel format GREY (gray scale 8bit)

If you want use other formats, change following variables.
- width, height in cap_cam.cpp (for width and height)
- V4L2_PIX_FMT_GREY in CameraCapture.cpp (for pixel format)

### use multiple camera
- see launch/multi_camera_launch.xml



## triorb_gamepad

### 概要
TriOrb AMR を市販/専用ゲームパッドから安全に操作する ROS 2 ノードを提供するパッケージです。`/dev/input/js*` を監視して対応デバイスを自動検出し、JSON で定義されたボタン/スティック割り当てに従って走行・リフタ・非常停止などのコマンドを生成します。ノード名やトピック名は `ROS_PREFIX` 環境変数を先頭に付与して重複を避けます。

### 提供ノード
#### `gamepad`
- `src/triorb_gamepad.cpp` の `_Node` クラスとして実装される単一ノードです。`UNIQUE_NODE` が有効なため同一名ノードが複数起動すると自動終了し、例外通知トピックへ状態を送出します。
- `dev` パラメータが空のときは `/dev/input/js0..js15` をスキャンして最初に反応したゲームパッドを使用します。
- ゲームパッド情報（名称・軸数・ボタン数）を読み込み、ユーザー辞書または `share/triorb_gamepad/params` のプリセットからマッピング設定を決定します。
- イベントループでは `AMRCtrl` 構造体に速度/加減速/リフタ状態を蓄積し、変化が生じたときのみ TriOrb RunVel コマンドを発行します。

##### モード管理
- 1 秒周期の `mode_check_timer` で購読者数を確認し、`/collab/wakeup` トピックに購読者がいる場合は「コラボレーションモード」に自動切替します。以後のコマンドは `/collab/...` 系トピックへ送出されます。
- `safe_run_mode` は `safe_drive/run_vel` もしくは `/collab/safe_drive/run_vel` の購読者が存在するか、直前に SafeRun モードだったかで判定されます。安全速度トピックが有効な場合は通常の `/drive/run_vel` ではなく SafeRun トピックへ速度メッセージを発行します。
- `active`/`inactive` コマンドによりゲームパッドの有効状態を明示でき、アクティブでない場合は速度を常に 0 とし、矛盾した状態が続くとデバイスを切断して再初期化させます。

### 購読インターフェース（Subscriber）
本ノードは ROS 2 上で購読するトピックを持たず、Linux のジョイスティックデバイス `/dev/input/js*` を唯一の入力源とします。外部アプリケーションからソフトウェア的に入力を与えたい場合は、仮想ジョイスティックにイベントを書き込むことで擬似的に「Subscriber」へ publish できます。

#### 外部からの呼び出し例
以下は `evemu-play` を用いて `/dev/input/js0` にボタン押下イベントを送る例です。`triorb_gamepad` ノードは実ジョイスティックと同様にイベントを受信し、対応するコマンドを実行します。

```bash
sudo apt install evemu-tools
sudo evemu-record /dev/input/js0 > /tmp/js0.desc   # 事前にデバイス定義を保存（初回のみ）
sudo evemu-play /dev/input/js0 <<'EOF'
E: 0.000000 1 304 1   # ボタンID304(例: Aボタン)押下
E: 0.010000 0 0 0
E: 0.050000 1 304 0   # ボタンを離す
E: 0.060000 0 0 0
EOF
```

仮想デバイスを自作する場合は `uinput` を使う Python/C++ スクリプトで同様のイベントを送出できます。ジョイスティックの軸やボタン番号は README 下部に記載した JSON 辞書に合わせる必要があります。

### パラメータ
| 名称 | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `dev` | string | `""` | 使用するデバイスファイル（例: `/dev/input/js1`）。空の場合は自動検出。 |
| `dict` | string | `/params/gamepad` | ユーザー定義のゲームパッド辞書を格納するディレクトリ。存在しない場合はノードが作成します。 |
| `acc_min` | int | `50` | `val_acc`/`val_dec` コマンドで生成される最小加速度 [ms]。 |
| `acc_max` | int | `10000` | 同最大加速度 [ms]。 |
| `vel_xy_min` | double | `0.0006` | 並進速度の最小値 [m/s]。 |
| `vel_xy_max` | double | `0.6` | 並進速度の最大値 [m/s]。 |
| `vel_w_min` | double | `0.00175` | 角速度の最小値 [rad/s]。 |
| `vel_w_max` | double | `1.75` | 角速度の最大値 [rad/s]。 |

> `robot_config` を辞書ファイル内に記述した場合は、上記パラメータよりもファイル側の値が優先されます。

### 発行トピック
#### 走行関連（標準モード）
- `/drive/run_vel` (`triorb_drive_interface/msg/TriorbRunVel3`): 並進/回転速度と加減速設定。`safe_run_mode` が true の場合は代わりに `/safe_drive/run_vel` を使用。
- `/safe_drive/run_vel` (`triorb_drive_interface/msg/TriorbRunVel3`): SafeRun 対応先への速度通知。
- `/drive/stop` (`std_msgs/msg/Empty`): 非常停止（E-Stop）要求。
- `/drive/sleep` (`std_msgs/msg/Empty`): 走行停止＆スリープ。
- `/drive/wakeup` (`std_msgs/msg/Empty`): 走行再開。
- `/drive/run_lifter` (`std_msgs/msg/String`): `"up"`, `"down"`, `"stop"` を通知。
- `/drive/set_life_time` (`std_msgs/msg/UInt16`): 予備。現状コマンド割当は定義されていません。

#### 走行関連（コラボレーションモード）
`/collab/drive/stop`, `/collab/sleep`, `/collab/wakeup`, `/collab/run_lifter`, `/collab/set_life_time`, `/collab/run_vel`, `/collab/safe_drive/run_vel` を標準モードと同じメッセージ型で発行します。

#### 例外通知
- `/except_handl/node/add` (`std_msgs/msg/String`): ノード登録通知。
- `/triorb/error/str/add` (`std_msgs/msg/String`): デバイス欠如・読み取り失敗などの致命的エラーを通知。
- `/triorb/warn/str/add` (`std_msgs/msg/String`): ゲームパッドの状態異常による切断など非致命的事象。

本パッケージはサービス／アクションを提供しません。

### ゲームパッドコマンド一覧
JSON 辞書内で使用する `name` に応じて次の処理が実行されます。

| コマンド名 | 内容 |
| --- | --- |
| `val_x` / `val_y` / `val_w` | スティックの値を -1.0 〜 1.0 に正規化し、それぞれ `vx`, `vy`, `vw` に適用。 |
| `val_acc` / `val_dec` | 指定範囲にリニアマップして `acc`/`dec` [ms] を更新。 |
| `val_vxy` / `val_vw` | 並進 / 角速度の最大値にリニアマップ。 |
| `acc_inc`, `acc_dec`, `dec_inc`, `dec_dec` | 100 ms 単位で加減速を微調整。 |
| `vel_vxy_inc`, `vel_vxy_dec`, `vel_vw_inc`, `vel_vw_dec` | 0.05 m/s、0.157 rad/s 単位で速度比率を変更。 |
| `wakeup`, `sleep` | ステート遷移。`sleep` 後は速度が 0 に固定。 |
| `lift_up`, `lift_down`, `lift_stop` | リフタ制御文字列を生成。連続押下は無視。 |
| `e_stop` | 押下時に `/drive/stop`（コラボ時は `/collab/drive/stop`）を即時発行。 |
| `active`, `inactive` | デバイスの状態監視に利用。アクティブでない場合は絶対に速度を出力しません。 |

コマンドに該当しない名称はログに `[Unknown cmd_name]` として出力されます。

### ゲームパッド辞書ファイル
- ファイル名は `<デバイス名>_<軸数>_<ボタン数>.json` とし、`dict` で指定したディレクトリ、または `share/triorb_gamepad/params` に配置します。例: `Generic X-Box pad_8_11.json`。
- 典型的な構造:

```json
{
  "name": "Generic X-Box pad",
  "axis_count": 8,
  "button_count": 11,
  "axis_cmds": [
    {"name": "val_x", "type": "analog", "min": -32767, "max": 32767},
    {"name": "val_y", "type": "analog", "min": 32767, "max": -32767},
    {"name": ["acc_dec", "dec_dec"], "type": "digital"}
  ],
  "button_cmds": [
    {"name": "lift_stop", "type": "digital"},
    {"name": ["vel_vxy_inc", "vel_vw_inc"], "type": "digital"}
  ],
  "robot_config": {
    "acc_min": 50,
    "acc_max": 10000,
    "vel_xy_min": 0.05,
    "vel_xy_max": 0.6,
    "vel_w_min": 0.1,
    "vel_w_max": 1.75
  }
}
```

- `axis_cmds`/`button_cmds` の要素数はデバイスが持つ軸・ボタン数と同じである必要があります。`name` を配列にすると 1 つの軸/ボタンに複数コマンドを割り当てられます。「未使用」は空文字列 `""` を指定してください。
- `type` が `analog` の場合は `min`/`max` を必ず設定します。`digital` の場合は押下時 (`value > 0`) にのみ実行されます。

### 利用手順
1. TriOrb ワークスペースで依存関係を満たした状態にし、`colcon build --packages-select triorb_gamepad` でビルドします。
2. ゲームパッドを接続し、必要であれば `~/.ros/gamepad` などの辞書格納先を用意し JSON を配置します。
3. `ros2 run triorb_gamepad triorb_gamepad --ros-args -p dict:=/home/robot/.ros/gamepad -p dev:=/dev/input/js0` のように実行します。
4. 起動時ログにデバイス名と割り当てが表示されます。意図したコマンドが発行されない場合は `axis_cmds`/`button_cmds` を確認してください。

### エラー時の挙動
- デバイスが見つからない／読み込み中に `ENODEV`/`EIO` が発生した場合は `_Node` が終了し、例外トピックに詳細を投稿します。
- 連続して不正値が送られ `need_disconnect()` が true になった場合は警告を発しデバイスを閉じて再検出します。
- ROS 2 ランタイムに致命的なエラーが無い限り、例外発生後も 1 秒待機して再接続を試みます。


## Package: triorb_streaming_image_cpp
このパッケージは、ROS 2 の `sensor_msgs/msg/Image` トピックから画像をサブスクリプションし、圧縮後に **MQTT トピックへ配信**するストリーミングノードです。 <br>
python版(triorb_streaming_images)の代替パッケージであり、処理負荷軽減のためv1.2.3から追加されました。

---

###  更新履歴

---

### Subscriber
####  `sensor_msgs/msg/Image`
- Topic: (可変)
- Type: sensor_msgs/msg/Image

### Publisher
####  MQTT 出力
- **Payload**: `.webp`, `.jpg`, `.png` 形式に圧縮 → Base64 文字列にエンコード
- **Topic**: `camera/stream`
- **Protocol**: `paho-mqtt` による MQTT publish

### Parameter
| param | note | type | default |
|----------|----------|----------|----------|
| mqtt_address | MQTT Broker Address | string | localhost |
| mqtt_port | MQTT Broker Port | int | 1883 |
| mqtt_client_id | MQTT Client ID | string | triorb_streamer_{PID} |
| mqtt_topic | MQTT Topic | string | camera/stream |
| topic_name_raw | ROS2 topic name | string | /camera0 |
| scale | Stream scale | double | 0.2 |
| fps | Stream fps | double | 1.0 |
| quality | Image quality | int | 20 |
| encode | Encode format | string | webp |

#### note
- CPU usage: jpg < webp << png
- network trafic: webp < jpg <<< png

## Package: triorb_camera_argus

### Subscriber
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

### Publisher
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

### Service
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

### Action
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

## Package: triorb_streaming_images
このパッケージは、ROS 2 の `sensor_msgs/msg/Image` トピックから画像をサブスクリプションし、圧縮後に **MQTT トピックへ配信**するストリーミングノードです。

---

###  v1.2.0 変更点

- **画像配信方式が MQTT に移行**しました（従来のWebSocket配信は廃止）
- ROS 2 トピックから受信した画像を `.webp` 形式で圧縮
- Base64 エンコードし、MQTT ブローカーへ配信します

---

### Subscriber
####  `sensor_msgs/msg/Image`
- Topic: (可変)
- Type: sensor_msgs/msg/Image

### Publisher
####  MQTT 出力
- **Payload**: `.webp` 形式に圧縮 → Base64 文字列にエンコード
- **Topic**: `camera/stream`
- **Protocol**: `paho-mqtt` による MQTT publish


## sick_safetyscanners_base
Provides an Interface to read the sensor output of a SICK
  Safety Scanner

## Sick_Safetyscanners_Base CPP Driver

### Table of contents

- [Supported Hardware](#supported-hardware)
- [Getting started](#getting-started)
- [API](#api)
- [Creators](#creators)

A CPP standalone Driver which reads the raw data from the SICK Safety Scanners and takes custom functions to publish the data.

### Supported Hardware
Supported are all microScan3, nanoScan3 and outdoorScan3 variants with Ethernet connection.

![ ](docs/images/safetyscanners.png  "Sick microScan3")



### Getting started

The driver will be released on this github repository, and can then be installed from source.

#### Prerequisites

* Linux
* Correctly setup SICK Safety Scanner
* Connected SICK Safety Scanner and a correctly setup ethernet network. Both the host and the sensor have to be in the same network.
* Installed libboost

#### Installation

For installation this github repository has to be cloned and afterwards installed. If a custom install directory is wanted use the -DCMAKE_INSTALL_PREFIX option to specify a path.

```bash
git clone https://github.com/SICKAG/sick_safetyscanners_base.git
cd sick_safetyscanners_base
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=<path to install folder> ..
make -j8
make install
```

#### Usage

To use the library in a driver the path of the installation has to be added to the cmake prefix path of your application. You can achieve this by using, bevor invoking cmake on your application.

```
export CMAKE_PREFIX_PATH=<path to install folder>
```

Afterwards the driver and the settings for the driver can be included with:
```
##include <sick_safetyscanners_base/SickSafetyscanners.h>
##include <sick_safetyscanners_base/Exceptions.h>
##include <sick_safetyscanners_base/Types.h>
##include <sick_safetyscanners_base/datastructure/CommSettings.h>
```

To get the driver up and running you need first to choose between the synchronous and asynchronous APIs based on your needs.

In the latter case you can also pass an instance of boost::asio::io_service to the constructor of the AsyncSickSafetyScanner. 


### API

#### Synchronous Client

In cases where you do not want the driver to spawn internal child threads to asynchronously process incomming sensor data you can use the ```SyncSickSafetyScanner``` class.

| Function                                                                                                                                                  | Information                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| SyncSickSafetyScanner<br>(sick::types::ip_address_t sensor_ip, <br>sick::types::port_t sensor_port, <br>sick::datastructure::CommSettings comm_settings); | Constructor call.                                                                                                                                    |
| bool isDataAvailable();                                                                                                                                   | Non-blocking call that indicates wheether sensor data is available to fetch via the receive-function from the internal sensor data receiving buffer. |
| const Data receive<br>(sick::types::time_duration_t timeout = boost::posix_time::pos_infin);                                                              | Blocking call to receive one sensor data packet at a time.                                                                                           |

Example
```
// Sensor IP and Port
std::string sensor_ip_str = "192.168.1.11";
sick::types::ip_address_t sensor_ip = boost::asio::ip::address_v4::from_string(sensor_ip_str);
sick::types::port_t tcp_port {2122};

// Prepare the CommSettings for Sensor streaming data
sick::datastructure::CommSettings comm_settings;
std::string host_ip_str = "192.168.1.9";
comm_settings.host_ip = boost::asio::ip::address_v4::from_string(host_ip_str);
comm_settings.host_udp_port = 0;

// Create a sensor instance
auto safety_scanner = std::make_unique<sick::SyncSickSafetyScanner>(sensor_ip, tcp_port, comm_settings);

// Receive one sensor data packet
auto timeout = boost::posix_time::seconds(5);
sick::datastructure::Data data = safety_scanner->receive(timeout);

// ...
```

#### Asynchronous Client

If you dont need restrict your client to work with single-threaded blocking receive calls in a strict sequential manner you can use the ```AsyncSickSafetyScanner``` class. The sensor data callback required by the constructor has the following signature
```
void callback(const sick::datastructure::Data& data);
```

| Function                                                                                                                                                  | Information                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| AsyncSickSafetyScanner<br>(sick::types::ip_address_t sensor_ip, <br>sick::types::port_t sensor_port, <br>sick::datastructure::CommSettings comm_settings, <br>sick::types::ScanDataCb callback); | Constructor call with custom data sensor callback.                                
| AsyncSickSafetyScanner<br>(sick::types::ip_address_t sensor_ip, <br>sick::types::port_t sensor_port, <br>sick::datastructure::CommSettings comm_settings,<br> boost::asio::ip::address_v4 interface_ip, <br>sick::types::ScanDataCb callback); | Constructor call with custom data sensor callback for multicast ip addresses.                                
| AsyncSickSafetyScanner<br>(sick::types::ip_address_t sensor_ip, <br>sick::types::port_t sensor_port, <br>sick::datastructure::CommSettings comm_settings, <br>sick::types::ScanDataCb callback, <br>boost::asio::io_service& io_service); | Constructor call. This variant allows the user to pass through an instance of boost::asio::io_service to get full control over the thread execution. In this case the driver is not spawning an internal child thread but relies on the user to perform regular io_service.run() operations and keep the service busy.
| void run(); | Starts to receive sensor data via UDP and passes the data to the callback as specified in the constructor.
| void stop(); | Stops all asynchronous receiving and processing operations.


Example
```
// Sensor IP and Port
std::string sensor_ip_str = 192.168.1.11
sick::types::ip_address_t sensor_ip = boost::asio::ip::address_v4::from_string(sensor_ip_str);
sick::types::port_t tcp_port {2122};

// Prepare the CommSettings for Sensor streaming data
sick::datastructure::CommSettings comm_settings;
std::string host_ip_str = "192.168.1.9"
comm_settings.host_ip = boost::asio::ip::address_v4::from_string(host_ip_str);
comm_settings.host_udp_port = 0;

// Define a sensor data callback
sick::types::ScanDataCb cb = [](const sick::datastructure::Data &data) {
    std::cout << "Number of beams: " << data.getMeasurementDataPtr()->getNumberOfBeams() << std::endl;
};

// Create a sensor instance
auto safety_scanner = std::make_unique<sick::AsyncSickSafetyScanner>(sensor_ip, tcp_port, comm_settings, cb);

// Special case if a multicast IP is seltected as host_ip
// std::string host_ip_str = "235.235.235.2"
// comm_settings.host_ip = boost::asio::ip::address_v4::from_string(host_ip_str);
// std::string interface_ip_str = "192.168.1.9"
// auto interface_ip = boost::asio::ip::address_v4::from_string(interface_ip_str);
// auto safety_scanner = std::make_unique<sick::AsyncSickSafetyScanner>(sensor_ip, tcp_port, comm_settings, interface_ip, cb);

// Start async receiving and processing of sensor data
safety_scanner->run();

// ... Do other stuff

// Stop async processing
safety_scanner->stop();
```

#### Parameters of Communication Settings

The parameters can be set using the setters of the CommSettings class. To set for example to host_ip the following function can be called.

```
sick::datastructure::CommSettings m_communication_settings;
m_communication_settings.setHostIp("192.168.1.100");
```

| Parameter Name       | API                                                                                                                                                                                 | Default      | Information                                                                                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| sensor_ip            | void setSensorIp(const std::string& sensor_ip);                                                                                                                                     | 192.168.1.11 | Sensor IP address. Can be passed as an argument to the launch file.                                                                                       |
| host_ip              | void setHostIp(const std::string& host_ip);                                                                                                                                         | 192.168.1.9  | Host IP address.  Can be passed as an argument to the launch file.                                                                                        |
| host_udp_port        | void setHostUdpPort(const uint16_t& host_udp_port);                                                                                                                                 | 0            | Host UDP Port.  Can be passed as an argument to the launch file.  Zero allows system chosen port.                                                         |
| publishing_frequency | void setPublishingFrequency(const uint16_t& publishing_frequency)                                                                                                                   | 1            | Publish every n_th scan, where n is the publishing frequency.  For a 25Hz laser, setting  to 1 makes it publish at 25Hz, to 2 makes it publish at 12.5Hz. |
| start_angle          | void setStartAngle(const uint32_t& start_angle)                                                                                                                                     | 0.0          | Start angle of scan in radians, if both start and end angle are equal, all angels are regarded.  0° is at the front of the scanner.                       |
| end_angle            | void setEndAngle(const uint32_t& start_angle)                                                                                                                                       | 0.0          | End angle of scan in radians, if both start and end angle are equal, all angels are regarded.  0° is at the front of the scanner.                         |
| channel_enabled      | void setEnabled(bool enabled);                                                                                                                                                      | true         | If the channel should be enabled                                                                                                                          |
| e_interface_type     | void setEInterfaceType(const uint8_t& e_interface_type)                                                                                                                             | 0            | Sets the interface type of the sensor <br>0: EFI-pro <br>1:  EtherNet/IP <br>3:  Profinet<br>4: Non-safe Ethernet                                         |
| features             | void CommSettings::setFeatures<br>(<br> bool general_system_state,<br> bool derived_settings, <br> bool measurement_data, <br> bool intrusion_data, <br> bool application_data<br>) | all true     | Enables the individual data outputs.                                                                                                                      |


#### COLA2 Functions (available on both driver API variants)

The Library allows to access variables of the sensor and invoke methods to change settings using the COLA2 protocol. The following methods can be called:

| Function                                                                                                                                                         | Information                                                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| void changeSensorSettings<br>(const sick::datastructure::CommSettings& settings)                                                                                 | Updates the sensor settings to the passed configuration.                                                                                                                                      |
| void findSensor<br>(<br>uint16_t blink_time);                                                                 | Lets the sensor flash the display for the specified time.                                                                                                                                    |
| void requestApplicationName<br>(sick::datastructure::ApplicationName& application_name);                  | Returns the name of the current application.                                                                                                                                                  |
| void requestConfigMetadata<br>(sick::datastructure::ConfigMetadata& config_metadata);                     | Returns the metadata of the current configuration of the sensor.                                                                                                                              |
| void requestDeviceName<br>(sick::datastructure::DeviceName& device_name);                                 | Returns the device name.                                                                                                                                                                      |
| void requestDeviceStatus<br>(sick::datastructure::DeviceStatus& device_status);                           | Returns the device status.                                                                                                                                                                    |
| void requestFieldData<br>(std::vector< sick::datastructure::FieldData>& field_data);                     | Returns the field data of the warning and safety fields.                                                                                                                                      |
| void requestFirmwareVersion<br>(sick::datastructure::FirmwareVersion& firmware_version);                  | Returns the firmware version.                                                                                                                                                                 |
| void requestLatestTelegram<br>(sick::datastructure::Data& data, <br> int8_t index = 0);                   | Returns the latest telegram for the channel index. Up to 4 Channels can be supported by the cola protocol, the actual number depends on the used scanner. Channel 0 is set as default value. |
| void requestMonitoringCases<br>(std::vector< sick::datastructure::MonitoringCaseData>& monitoring_cases); | Returns the data of the Monitoring Cases.                                                                                                                                                    |
| void requestOrderNumber<br>(sick::datastructure::OrderNumber& order_number);                              | Returns the order Number.                                                                                                                                                                     |
| void requestPersistentConfig<br>(sick::datastructure::ConfigData& config_data);                           | Returns the Persistent configuration of the sensor, which was set in the Safety Designer.                                                                                                     |
| void requestProjectName<br>(sick::datastructure::ProjectName& project_name);                              | Returns the project name.                                                                                                                                                                     |
| void requestRequiredUserAction<br>(sick::datastructure::RequiredUserAction& required_user_action);       | Returns the required user actions as specified in the cola 2 manual.                                                                                                                         |
| void requestSerialNumber<br>(sick::datastructure::SerialNumber& serial_number);                           | Returns the serial number of the sensor.                                                                                                                                                      |
| void requestStatusOverview<br>(sick::datastructure::StatusOverview& status_overview);                     | Returns the status overview.                                                                                                                                                                  |
| void requestTypeCode<br>(sick::datastructure::TypeCode& type_code)                                 | Returns the type code of the sensor.                                                                                                                                                          |
| void requestUserName<br>(sick::datastructure::UserName& user_name);                                       | Returns the user name.                                                                                                                                                                        |

#### Troubleshooting

* Check if the sensor has power and is connected to the host.
* Check if both sensor and host are in the same subnet e.g. 192.168.1
* Are the correct IPs configured for the application?
* Is the correct Interface Type configured?





### Creators

**Lennart Puck** <br>
**Martin Schulze**

FZI Forschungszentrum Informatik


- <http://www.fzi.de>

on behalf of SICK AG 

- <http://www.sick.com>






## Package: triorb_sick_flexi_soft

### Subscriber
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

### Publisher
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

### Service
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

### Action
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

## Package: triorb_sick_plc_wrapper

### Subscriber
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

### Publisher
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

### Service
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

### Action
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

## sick_safetyscanners2_interfaces
Interfaces for the sick_safetyscanners ros2 driver

## SICK Safetyscanner ROS2 Interfaces

This package contains the necessary interfaces used for the ROS2 driver for the SICK Safetyscanners.

It includes message and service definitions for:
* Extended Laser Scan
  * Includes detected reflectors.
* Output Paths
  * Gives the status if the currently configured output paths. 
* Raw Data
  * Gives all data currently provided by the sensor for further processing.
* Field Data
  * A service returning the protective and warning field geometries with a mapping to the respective
    output paths.


## sick_safetyscanners2
ROS2 Driver for the SICK safetyscanners

## Sick_Safetyscanners ROS2 Driver

A ROS2 Driver which reads the raw data from the SICK Safety Scanners and publishes the data as a laser_scan msg.

The ROS1 Driver can be found here: https://github.com/SICKAG/sick_safetyscanners

### Table of contents

- [Supported Hardware](#supported-hardware)
- [Getting started](#getting-started)
- [ROS API](#ros-api)
- [Creators](#creators)


### Supported Hardware

Supported are all microScan3, nanoScan3 and outdoorScan3 variants with Ethernet connection.

![ ](docs/images/safetyscanners.png  "Sick Safetyscanner Family")



### Getting started
In the future the ROS2 driver will be released as a debian package, currently only build from source
is supported.

#### Prerequisites

* Linux
* Working ROS-Distro
* Correctly setup SICK Safety Scanner
* Connected SICK Safety Scanner and a correctly setup ethernet network. Both the host and the sensor have to be in the same network.

#### Installation

##### Dependencies

Dependencies can be installed via 
```
sudo apt-get install ros-<rosdistro>-sick-safetyscanners2-interfaces
sudo apt-get install ros-<rosdistro>-sick-safetyscanners-base
```

The sources can be found here:
* sick_safetyscanners_base (https://github.com/SICKAG/sick_safetyscanners_base)
* sick_safetyscanners2_interfaces (https://github.com/SICKAG/sick_safetyscanners2_interfaces)


##### From Source

```bash
source /opt/ros/<rosdistro>/setup.bash
mkdir -p ~/colcon_ws/src/
cd ~/colcon_ws/src/
git clone https://github.com/SICKAG/sick_safetyscanners2.git
cd ..
colcon build --symlink-install
source ~/colcon_ws/install/setup.sh
```

#### Starting

##### Classic Node

To start the driver the launch file has to be started. For the driver to work correctly, the sensor ip and host ip have to be defined. These parameters can be passed to the sensor as arguments via launch file.

```
ros2 launch sick_safetyscanners2 sick_safetyscanners2_launch.py
```

This will start the driver with the in launch file defined parameters.

##### Lifecycle Node

To start the driver within a lifecycle the launch file has to be started. For the driver to work correctly, the sensor ip and host ip have to be defined. These parameters can be passed to the sensor as arguments via launch file.

```
ros2 launch sick_safetyscanners2 sick_safetyscanners2_lifecycle_launch.py
```

This will start the driver with the in launch file defined parameters.

To configure and activate the lifecycle node the following commands have to be issued:
```
// Configure
ros2 lifecycle set /sick_safetyscanners2_lifecycle_node configure

//Activate
ros2 lifecycle set /sick_safetyscanners2_lifecycle_node activate
```


##### Visualization

To visualize the data start rviz2 and subscribe to the ~/scan topic.
By default the frame_id is "scan" however this can be customized in the launch file

```
rviz2
```

#### Troubleshooting

* Check if the sensor has power and is connected to the host.
* Check if both sensor and host are in the same subnet e.g. 192.168.1
* Check if the launch file is called with the correct parameters for IP-addresses and ports.

### ROS2 API



#### Advertised ROS2 Topics


`
~/scan (type: sensor_msgs/msg/LaserScan)
`

Publishes a scan from the laserscanner

`
~/extended_laser_scan (type: sick_safetyscanners2_interfaces/msg/ExtendedLaserScan)
`

Extends the basic laser scan message by reflector data and intrusion data.

`
~/output_paths (type: sick_safetyscanners2_interfaces/msg/OutputPath)
`

Gives feedback of the current status of the output paths.


`
~/raw_data (type: sick_safetyscanners2_interfaces/msg/RawMicroScanData)
`

Publishes the raw data from the sensor as a ROS2 message.

`
~/diagnostics (type: diagnostic_msgs/msg/DiagnosticArray)
`

Frequency and sensor diagnostics

#### Advertised ROS2 Services

`
~/field_data
`

Returns all configured protective and warning fields for the sensor


`
~/status_overview
`

Returns the status overview of the sensor.
[There is further information of error codes.](docs/error_handling.md#error-codes)

#### ROS2 parameters

| Parameter Name        | Type    | Default      | Required on startup | Information                                                                                                                                                                                                                                |
| -------------         | ------  | -------      | ------------        | -------------                                                                                                                                                                                                                              |
| sensor_ip             | String  | 192.168.1.11 | ✔                   | Sensor IP address. Can be passed as an argument to the launch file.                                                                                                                                                                        |
| host_ip               | String  | 192.168.1.9  | ✔                   | Host IP address.  Can be passed as an argument to the launch file.                                                                                                                                                                         |
| interface_ip          | String  | 0.0.0.0      |                     | Interface IP address of the receiving host computer, this needs to be set if the host IP is in the multicast IP range. The default is an undefined IP address and will return an error when multicast is used without a correct interface. |
| host_udp_port         | Integer | 0            |                     | Host UDP Port.  Can be passed as an argument to the launch file.  Zero allows system chosen port.                                                                                                                                          |
| frame_id              | String  | scan         |                     | The frame name of the sensor message                                                                                                                                                                                                       |
| skip                  | Integer | 0            |                     | The number of scans to skip between each measured scan.  For a 25Hz laser, setting 'skip' to 0 makes it publish at 25Hz, 'skip' to 1 makes it publish at 12.5Hz.                                                                           |
| angle_start           | Double  | 0.0          |                     | Start angle of scan in radians, if both start and end angle are equal, all angels are regarded.  0° is at the front of the scanner.                                                                                                        |
| angle_end             | Double  | 0.0          |                     | End angle of scan in radians, if both start and end angle are equal, all angels are regarded.  0° is at the front of the scanner.                                                                                                          |
| min_intensities       | Double  | 0.0          |                     | If this parameter is set, all points below the one set in the parameter are set to infinity                                                                                                                                                |
| channel_enabled       | Boolean | true         |                     | If the channel should be enabled                                                                                                                                                                                                           |
| general_system_state  | Boolean | true         |                     | If the general system state should be published                                                                                                                                                                                            |
| derived_settings      | Boolean | true         |                     | If the derived settings should be published                                                                                                                                                                                                |
| measurement_data      | Boolean | true         |                     | If the measurement data should be published                                                                                                                                                                                                |
| intrusion_data        | Boolean | true         |                     | If the intrusion data should be published                                                                                                                                                                                                  |
| application_io_data   | Boolean | true         |                     | If the application IO data should be published                                                                                                                                                                                             |
| use_persistent_config | Boolean | false        |                     | If this flag is set, the configured angles from the sensor are loaded and used and the ROS parameters *angle_start* and *angle_end* are disregarded                                                                                        |

### Creators

**Lennart Puck** 

FZI Forschungszentrum Informatik


- <http://www.fzi.de>

on behalf of SICK AG 

- <http://www.sick.com>






## triorb_sls_wrapper

    Convert SICK SLS RawMicroScanData topics into sensor_msgs/PointCloud messages.
  

﻿# SICK SLS データツール

SICK SLS センサから取得した `raw_data.log` を可視化し、ROS 2 互換の占有グリッドへ変換する Python スクリプト群です。センサの検出補償範囲（minimum detectable free space）は 3.0 m と仮定し、+Inf を返したビームも走行可能領域として扱えます。

### 必要環境

- Python 3.9 以上
- [PyYAML](https://pyyaml.org/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Pillow](https://python-pillow.org/)（任意。PNG 出力に利用）

インストール例:

```bash
pip install pyyaml numpy matplotlib pillow
```

> Pillow が無い場合、`generate_occupancy.py` は Matplotlib を利用して PNG を保存します。

### /sick/raw_dataをサブスクライブしてPointCloudをPublishするノード（`src/raw_data_to_pointcloud_node.cpp`）
ROS 2 ノードとして動作し、`/sick/raw_data` トピックからデータを受信して、serial-numberが一致したデータをPointCloud2メッセージとしてパブリッシュします。オフセット値はミリメートル単位で指定します。シリアル番号ごとのキャリブレーション値は JSON ファイルにまとめて読み込み、`serial_number_of_device` に応じて自動で切り替わります。

`config/sls_point2d_config.json`（インストール後は`share/triorb_sls_wrapper/config/`配下）を編集してください:

```json
{
  "default": {
    "angle_offset": 0.0,
    "offset_x": 0.0,
    "offset_y": 0.0,
    "pointcloud_topic": "/sick/point2d"
  },
  "24050147": {
    "angle_offset": 290.0,
    "offset_x": 170.0,
    "offset_y": 156.0,
    "pointcloud_topic": "/sick/point2d47"
  },
  "24050160": {
    "angle_offset": 70.0,
    "offset_x": -170.0,
    "offset_y": 156.0,
    "pointcloud_topic": "/sick/point2d52"
  }
}
```

`pointcloud_topic` を省略した場合は `default` セクションの値が利用されます。`ROS_PREFIX` 環境変数が設定されている場合は接頭辞付きでトピックが生成されます。

```bash
colcon build && source install/setup.bash &&\
ros2 run triorb_sls_wrapper sls_point2d \
  --ros-args \
  -p config_file:=$(ros2 pkg prefix triorb_sls_wrapper)/share/triorb_sls_wrapper/config/sls_point2d_config.json
```

特定センサのみ処理したい場合は `-p serial_number:=<value>` と `-p filter_by_serial:=true` を併用してください。既定（`serial_number<=0`）では全シリアルを受け付け、JSONで定義されていないシリアルは `default` セクションの補正値が適用されます。

### /sick/raw_dataを占有グリッドへ変換するノード（`src/raw_data_to_occupancy_node.cpp`）

`/sick/raw_data` を購読し、スキャンごとに `nav_msgs/msg/OccupancyGrid` を生成してパブリッシュします。`generate_occupancy.py` のロジックをROS 2ノード化したもので、シリアル番号ごとに解像度や検知範囲、出力トピックを切り替えられます。

`config/sls_occupancy_config.json`（インストール後は`share/triorb_sls_wrapper/config/`配下）を編集してください:

```json
{
  "default": {
    "angle_offset": 0.0,
    "offset_x": 0.0,
    "offset_y": 0.0,
    "unit_scale": 0.001,
    "resolution": 0.05,
    "margin": 0.5,
    "xy_limit": 5.0,
    "detection_range": 10.0,
    "max_range": null,
    "beam_group_size": 4,
    "frame_id": "map",
    "occupancy_topic": "/sick/occupancy"
  },
  "24050160": {
    "angle_offset": 70.0,
    "offset_x": -170.0,
    "offset_y": 156.0,
    "xy_limit": 6.0,
    "beam_group_size": 4,
    "occupancy_topic": "/sick/occupancy52"
  }
}
```

`occupancy_topic` を省略した場合は `default` の値が利用されます。`ROS_PREFIX` 環境変数を指定すると接頭辞付きトピックへ自動変換されます。

`detection_range` は +Inf ビームに対しても自由セルとして扱う最大距離を表し、範囲内は占有率 0 で塗りつぶされます。`beam_group_size` は角度方向のビームをまとめる単位数で、各グループの中から最も近い障害物を含むビーム（なければ任意のビーム）が選択されるため、計算負荷を抑えつつ近距離の障害物を優先的に反映できます。

```bash
colcon build && source install/setup.bash &&\
ros2 run triorb_sls_wrapper sls_occupancy \
  --ros-args \
  -p config_file:=$(ros2 pkg prefix triorb_sls_wrapper)/share/triorb_sls_wrapper/config/sls_occupancy_config.json
```

`-p serial_number:=<value>` と `-p filter_by_serial:=true` を併用すれば、特定センサのみOccupancyGridを生成します。定義済みシリアルが1件だけの場合は自動でその設定が選択されます。

#### OccupancyGridをPNGとして保存するテストスクリプト

`test/save_occupancy_png.py` を利用すると、任意の占有グリッドトピックを購読して最初のメッセージをPNGとして保存できます。Pillow (`pip install pillow`) を事前にインストールしてください。

```bash
python3 test/save_occupancy_png.py \
  --topic /sick/occupancy52 \
  --output occupancy_snapshot.png
```

未知セル (-1) は灰、自由セル (0) は白、占有セル (100) は黒で描画されます。メッセージを1度受信すると自動的にノードが終了します。

### /sick/raw_dataをサブスクライブしてプロット（`plot_raw_data_node.py`）

パラメータは`plot_raw_data.py`と同様ですが、ROS 2 ノードとして動作し、`/sick/raw_data` トピックからデータを受信して、serial-numberが一致したデータをプロットします。オフセット値はミリメートル単位で指定します。

```bash
tmux new-session -s play -d "ros2 bag play -l test/rosbag2_2025_11_05-00_06_02/"
python plot_raw_data_node.py \
  --output raw_data_node_plot.svg \
  --serial-number 24050160 \
  --angle-offset 70 \
  --offset-x -170 \
  --offset-y 156
```

### raw_data のプロット (`plot_raw_data.py`)

極座標ビューと XY ビューを生成し、反射率つきでスキャン結果を確認します。オフセット値はミリメートル単位で指定します。

```bash
python plot_raw_data.py \
  --input raw_data.log \
  --output raw_data_plot.svg \
  --angle-offset 70 \
  --offset-x -170 \
  --offset-y 156 \
  --xy-limit 2000 \
  --dpi 1200
```

#### 主なオプション

- `--angle-offset` センサ取り付け角度の補正（度、時計回りが正）。
- `--offset-x`, `--offset-y` センサ位置の平行移動量（ミリメートル）。`offset-y` の正値で下方向にシフト。
- `--xy-limit` XY ビューの表示範囲（ミリメートル）。例: `2000` で ±2000 mm を描画。
- `--dpi` 画像保存時の解像度。高くすると詳細になるがファイルサイズも増加。
- `--show` 生成後に Matplotlib ウィンドウを表示。

Polar View には 0.1 ステップの補助円を追加、XY View は等倍率で描画します。

### 占有グリッド生成 (`generate_occupancy.py`)

`raw_data.log` から ROS 2 `nav_msgs::msg::OccupancyGrid` 互換の PNG と JSON メタデータを出力します。センサオフセットはミリメートル、その他の距離系はメートルで指定します。

```bash
python generate_occupancy.py \
  --input raw_data.log \
  --output occupancy_map.png \
  --output-meta occupancy_map.json \
  --resolution 0.03 \
  --unit-scale 0.001 \
  --angle-offset 70 \
  --offset-x -170 \
  --offset-y 156 \
  --infinite-free-range 3.0 \
  --detection-range 10.0 \
  --xy-limit 5.0 \
  --dpi 600
```

#### 主なパラメータ

- `--resolution` グリッド解像度（メートル/セル）。既定値は 0.01。
- `--unit-scale` 距離の単位変換。ミリ -> メートルなら 0.001。
- `--xy-limit` センサ中心の正方形領域を ±値メートルでクリップ。未指定ならスキャン範囲に余白を加えて自動計算。
- `--margin` `--xy-limit` 未指定時に周囲へ加える余白（メートル）。
- `--max-range` 指定距離を超える計測値を除外（メートル）。
- `--angle-offset` 角度補正（度）。`plot_raw_data.py` と同じ値を推奨。
- `--offset-x`, `--offset-y` センサ位置の補正量（ミリメートル）。内部で `unit-scale` によりメートルへ換算。
- `--infinite-free-range` +Inf（飽和）ビームに対して最低限走行可能とみなす距離（メートル）。既定値は 3.0 m（SICK 検出補償範囲）。
- `--detection-range` 3.0 m から 10.0 m までを検出可能範囲とみなし、距離に応じて占有率 0~50 を割り当てます。
- `--output-meta` ROS 用メタデータ (JSON) を保存。
- `--show` Matplotlib を使って占有グリッドを表示。

#### 出力

- **occupancy_map.png**: 占有セル (100) は黒、自由セル (0) は白、未知セル (-1) は灰。画像は ROS の座標系に合わせて下向き原点で保存。
- **occupancy_map.json**: `resolution`、`width`、`height`、`origin` など `nav_msgs::msg::OccupancyGrid::info` に転記可能な情報を含む。

ROS 2 側では画像を行優先（row-major）で読み込み、`origin` を踏まえて `data` 配列へ展開してください。

### 運用のヒント

- 角度・平行移動オフセットは両スクリプトで統一すると結果が揃います。
- 高 DPI 設定はファイルサイズが大きくなるため用途に応じて調整してください。
- `--max-range` や `--infinite-free-range` を活用して、走行可能領域の解像度と範囲のバランスを取ってください。


## Package: triorb_navigation_manager

### 概要

`triorb_navigation_manager`はTriOrb AMR向けのROS 2ノードであり、CSVで定義された経路に従ってナビゲーション・協調走行・リフター動作・TagSLAM/SLAM連携・安全装置制御・イベント連携を一元管理します。ROS 2 TopicとMQTTの双方を用いて外部モジュールと連携し、状態監視や再開制御、地図切替待機などを自動化します。ノード起動時に一意性チェックを行い、`ROS_PREFIX`に応じた名前空間付きトピックへ自動的に接続します。

### 主な機能

- 経路CSV（`/data/route/<name>.csv`）のロード・解析とWayPoint管理（Start/End行を基準に自動抽出）
- `nav/action`での開始・停止・一時停止・失敗復帰指示、速度係数や精度バイアスの適用
- 走行（通常/協調/TagSLAM/相対移動）・リフター・イベント・地図操作・安全装置操作など多様なアクションを組み合わせ可能
- Drive/Lifter/MQTTイベントの成功判定と`NavResult`コードによる結果通知、失敗時は復帰位置を保持
- `/triorb/nav/state`によるナビゲーション状態公開と`/triorb/request_nav_state`からの即時再送
- MQTT経由での地図待機時間取得・読み込みスキップ・VSLAM制御

### CSVベースの経路定義

- ファイル配置: 既定で`/data/route/`配下。拡張子が無い場合は自動的に`.csv`を付与。
- 行形式: `type,name,action,x,y,w,vxy,vw,acc_xy,acc_w,gain,camera,accel_ms,...`
- `type`が`route/Start`と`route/End`の行で経路範囲を自動決定。
- `accel_ms`が未設定の場合は`DEFAULT_ACC=1000`、速度比は`nav/action`コマンドで与えた`ratio_speed`を乗算。
- `check_waypoints`で`acc_xy`または`acc_w`がバイアス加算後に0以下の場合は開始前にエラー通知。

#### 代表的な`type`と動作

| type | 内容 | 使用トピック |
| --- | --- | --- |
| `point` `into` | 絶対座標走行。`into`はTagSLAM側ポーズ設定。 | `/drive/set_pos` `/tagslam/drive/set_pos` |
| `collab*` | 協調搬送系。 | `/collab/request/set_pos` |
| `relative` | 相対移動。 | `/drive/run_pos` |
| `リフター` / `協調リフト` | 単体/協調リフター命令。 | `/drive/run_lifter` `/collab/run_lifter` |
| `一時停止` | 指定秒数待機。 | 内部タイマー |
| `イベント発行` / `イベント待ち` | `/action/event` によるイベント送受信。 | `/action/event` |
| `地図切替` / `地図遷移` | MQTTでVSLAM制御 または `/run_slam/set/enter_local_map_file_path` へ通知。 | `vslam/signal` 他 |
| `地図切替(TagSLAM)` | `/tagslam/load/map`へJSONを送信。 | `/tagslam/load/map` |
| `マーカー設定` | MarkerSetting(default/only/exclude)切替。 | `/run_slam/set/marker_only` `/run_slam/set/marker_exclude` |
| `安全装置起動/停止` | SLSブレーキ制御。 | `/sls/set/brake` |
| `減速範囲設定` | フィールドID(10進/0xNN)を`UInt8`変換して送出。 | `/sls/set/field` |

### ノードAPI

#### Subscriber

| Topic | 型 | 役割 |
| --- | --- | --- |
| `/nav/route_csv_name` | `std_msgs/msg/String` | CSVファイル名を受け取りWayPointを再ロード。 |
| `/nav/action` | `std_msgs/msg/String` | `start`/`stop`/`pause`/`resume`/`resume_failed` コマンド。 |
| `/drive/result` | `triorb_drive_interface/msg/TriorbRunResult` | 通常走行結果。 |
| `/collab/drive/completed` | `triorb_drive_interface/msg/TriorbRunResultStamped` | 協調走行結果。 |
| `/drive/run_pos/result` | `std_msgs/msg/String` | 相対移動結果（"done"等）。 |
| `/lifter/result` | `std_msgs/msg/String` | 単体リフター結果。 |
| `/collab/lifter/result` | `std_msgs/msg/String` | 協調リフター結果（JSON文字列）。 |
| `/action/event` | `std_msgs/msg/String` | イベント待ちモードで一致イベントを待受。 |
| `/triorb/request_nav_state` | `std_msgs/msg/Empty` | 状態再送指示。 |
| `/run_slam/map_file_changed` | `std_msgs/msg/String` | 地図ファイル変更通知、地図待機解除に使用。 |

##### 呼び出し例

```bash
## 経路CSVをsample_route.csvへ切替
ros2 topic pub /nav/route_csv_name std_msgs/msg/String "data: 'sample_route.csv'"

## 速度倍率1.0、精度バイアス0、1ループで走行開始
ros2 topic pub /nav/action std_msgs/msg/String "data: 'start,1.0,0.0,0.0,1'"

## 協調走行結果はechoで監視
ros2 topic echo /collab/drive/completed

## リフター完了通知を監視
ros2 topic echo /lifter/result

## イベント待ちアクションに合致させるイベントを送信
ros2 topic pub /action/event std_msgs/msg/String "data: 'door_opened'"

## 最新のナビゲーション状態をリクエスト
ros2 topic pub /triorb/request_nav_state std_msgs/msg/Empty "{}"
```

#### Publisher

| Topic | 型 | 役割 |
| --- | --- | --- |
| `/nav/handling_task_csv_name` | `std_msgs/msg/String` | 現在処理中のCSV名を通知。 |
| `/triorb/nav/state` | `std_msgs/msg/Int32MultiArray` | ナビ状態／エラー／復帰情報。 |
| `/triorb/nav/result` | `std_msgs/msg/String` | `NavResult&&詳細` 形式の結果通知。 |
| `/drive/init_path_follow` `/collab/drive/init_path_follow` `/tagslam/drive/init_path_follow` | `std_msgs/msg/Empty` | 各経路制御モジュールの初期化。 |
| `/drive/set_pos` `/tagslam/drive/set_pos` `/collab/request/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | 走行目標の送信。 |
| `/drive/run_pos` | `triorb_drive_interface/msg/TriorbRunPos3` | 相対移動指示。 |
| `/drive/pause` `/drive/restart` `/drive/stop` ほか`/collab/drive/*` | `std_msgs/msg/Empty` | 走行制御。 |
| `/drive/run_lifter` `/collab/run_lifter` | `std_msgs/msg/String` | リフター指示。 |
| `/action/event` | `std_msgs/msg/String` | イベント発行。 |
| `/run_slam/set/enter_local_map_file_path` | `std_msgs/msg/String` | 地図遷移時に使用。 |
| `/run_slam/set/marker_only` `/run_slam/set/marker_exclude` | `std_msgs/msg/Bool` | MarkerSetting切替。 |
| `/tagslam/load/map` | `std_msgs/msg/String` | TagSLAM用地図切替（JSON文字列）。 |
| `/sls/set/brake` | `std_msgs/msg/Bool` | SLSブレーキON/OFF。 |
| `/sls/set/field` | `std_msgs/msg/UInt8` | 減速エリア設定。 |
| `/except_handl/node/add` `/triorb/error/str/add` `/triorb/warn/str/add` | `std_msgs/msg/String` | 例外監視システムへの登録/エラー/警告送信。 |

#### Service

| Service | 型 | 内容 |
| --- | --- | --- |
| `/get/version/<node_name>` | `triorb_static_interface/srv/Version` | ノードバージョン（`1.2.2`）を配列で返却。 |

#### MQTT

| Topic | 向き | 内容 |
| --- | --- | --- |
| `/vslam/map_load_queuing_time_estimated` | Subscribe | マップ読込推定時間（秒）。 |
| `/vslam/map_skip_loading_request` | Subscribe | 地図読込スキップ要求。 |
| `vslam/signal` | Publish | `load_<map>` メッセージでVSLAMへ地図切替指示。 |

### コマンド/メッセージ仕様

#### `/nav/action`

- `start,<ratio_speed>,<bias_xy>,<bias_deg>,<loop>`  
  例: `start,1.0,0.0,0.0,1`。Start/End行間のWayPointをloop回だけ走行。
- `stop` / `pause` / `resume` は通常の停止および一時停止制御。
- `resume_failed` は失敗時に保持した`resume_pos_idx`から再開。`enter_failure_hold_state`で保持される。

#### `/triorb/nav/state` (`std_msgs/msg/Int32MultiArray`)

配列構造: `[state, loop_count, loop, pos_idx, markerSetting, error_pair_count, error_list..., resume_pos_idx, resume_available_flag]`

- `state`: `NavState` (`0:IDLE / 1:NAVIGATING / 2:PAUSED`)
- `markerSetting`: `0:default / 1:only / 2:exclude`
- `error_list`: 2要素で1組（WayPoint行番号, 種別コード 0:角度精度 1:XY精度 2:双方）
- `resume_available_flag`: 1の場合`resume_failed`で再開可

#### `/triorb/nav/result`

`<NavResult>&&<詳細>` 形式。代表値:

| NavResult | 意味 |
| --- | --- |
| `SUCCESS` | 経路完遂 |
| `NAV_FAILED` | 走行系エラー（`msg_to_json_string`で詳細付与） |
| `USER_CANCELLED` | `stop`指示で終了 |
| `ROUTE_ERROR` `WAYPOINT_SETTING_ERROR` など | 入力CSV関連 |
| `LIFTER_ERROR` | リフター失敗 |
| `MAP_LOAD_TIME_OUT_ERROR` | 地図切替タイムアウト |
| `UNKNOW_ACTION_ERROR` ほか | 想定外アクション |

アクション失敗時は`enter_failure_hold_state`で停止し、成功時は`check_compleated_operation`で次WayPointまたはLoop切り替えを実施。

### エラー・状態管理

- `reset_nav()`でWayPointポインタ、速度係数、バイアス、待機フラグ、エラーリスト、地図状態を初期化。
- タイマー (`0.5s`) で状態を定期送信。`/triorb/request_nav_state`受信時は即時再送。
- 地図切替時はMQTT推定時間を待機し、タイムアウトすると`MAP_LOAD_TIME_OUT_ERROR`を通知してナビゲーションをリセット。
- `wait_nav`などのフラグにより並列アクションを制御し、完了コールバックで次のWayPoint処理を進める。

### 運用上の注意

- ノード名はファイル名先頭の`_`を除き、`ROS_PREFIX`付きで決定されます。ノード起動時に同名ノードが存在すると起動を中止します。
- CSVには最低1つ以上のWayPoint（Start/End以外）が必要です。`idx_start >= idx_end`またはWayPoint不足の場合は`WAYPOINTS_EMPTY_ERROR`を返します。
- `MarkerSetting`はトピック送信直後に`/triorb/nav/state`へ反映されるため、UI側で状態確認してください。
- MQTTブローカー（既定: `localhost:1883`）に接続できない場合、地図切替アクションが正常に完了しません。必要に応じて`MQTTClient.connect()`のログを確認してください。


## Package: triorb_drive_pico
モーターの制御ECUと通信し, 移動指示の送信やステータス取得するためのパッケージ. 

### 主な機能
- 移動指示によるロボットの駆動
- ロボットの内部状態の通知

### 更新履歴
#### 1.2.3
- 現在実行中の指令が分かるように/drive/mode topicを追加
- /drive/run_pos/result topicを追加し, 相対移動完了を通知するように変更

#### 1.2.0
- 各バージョン取得serviceをtopicに変更、10秒に1回publishするように変更
- picoから最大速度・最小速度を取得し、Jetson内に保存するコードを追加
- picoからエラー履歴を取得するservice追加
- 特定の条件で速度指示を無視していたバグ修正

#### 1.1.0
- nodeのバージョン取得serviceを追加（有効になるようにバグ修正）
- picoのバージョン取得serviceを追加
- triorb_coreのバージョン取得serviceを追加
- 励磁オン・オフのservice版を追加
- 速度0命令は連続でない限りスキップしない

### Subscriber

#### 励磁オン
- Topic: (prefix)/drive/wakeup
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/wakeup std_msgs/msg/Empty 
```

#### 励磁オフ
- Topic: (prefix)/drive/sleep
- Type: std_msgs/msg/Empty
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/sleep std_msgs/msg/Empty
```

#### 速度ベクトル指示による移動
- Topic: (prefix)/drive/run_vel
- Type: triorb_drive_interface/msg/TriorbRunVel3
- Note: 前回適用された指示と比較して, 以下の条件を両方満たす場合はスキップする.
    - 0.2秒以下の間隔
    - 速度指示値velocityのx,y,wの差が0.001以下

#### 移動距離指示による相対移動
- Topic: (prefix)/drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3

#### モータードライバの設定変更
- Topic: (prefix)/set/motor/params
- Type: triorb_drive_interface/msg/MotorParams
- Note: 全ての値を0にすると, 出荷時の設定を書き込む.

#### 移動停止
- Topic: (prefix)/drive/stop
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/stop std_msgs/msg/Empty
```

#### トルク設定変更
- Topic: (prefix)/set/motor/torque
- Type: std_msgs/msg/Float32
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /set/motor/torque std_msgs/msg/Float32 "data: 100.0" # 10%
```

#### ライフタイムの設定
- Topic: (prefix)/drive/set_life_time
- Type: std_msgs/msg/UInt16
- Note: ライフタイム[ms]を設定する. 速度ベクトル指示後, ロボットはライフタイム経過後にエラー扱いで停止する. この時間は速度ベクトル指示の度に0からカウントされる. 0を設定すると無効になる.
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/set_life_time std_msgs/msg/UInt16 "data: 1000" # 1000ms
```

#### 運転モード
- Topic: (prefix)/mutex/set_drive_mode
- Type: std_msgs/msg/UInt8
- Note: 速度ベクトル指示での制御を変更する. 
 - 16: 速度制御. モーターは加速時間にしたがって加速し, 減速時間にしたがって減速する. 指示の与え方によっては意図しない回転成分が入るため非推奨.
 - 17: 押し当て制御. 負荷に押し当たった場合に加圧を続ける. トルクは100%に制限される.
 - 19: サイクリック制御（デフォルト）. 他の制御方式と比較して, 意図しない回転成分が入りにくい.
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /mutex/set_drive_mode std_msgs/msg/UInt8 "data: 16"
```

#### リフトアップ/リフトダウン
- Topic: (prefix)/drive/run_lifter
- Type: std_msgs/msg/String
- Note: リフター付きモデル限定.
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/run_lifter std_msgs/msg/String "data: up"
```

### Publisher

#### ロボットステータスの定期送信
- Topic: (prefix)/robot/status
- Type: triorb_static_interface/msg/RobotStatus
- Note: 1.5秒間隔で送信される.
- Note： Accepting move instruction, Generating mapフラグおよびvoltageは未実装 
```bash
triorb@orin-nx-XXX:~/$ ros2 topic echo --once /robot/status 
header: 
  stamp: 
    sec: 1717491443 
    nanosec: 313522765 
  frame_id: robot 
voltage: 0.0 
btns: 0 
state: 53248 
error: 0
```

#### オドメトリの定期送信
- Topic: (prefix)/triorb/odom
- Type: geometry_msgs/msg/Vector3Stamped
- Note: 0.2秒間隔で送信される.


#### バージョン情報の定期送信
- Topic: (prefix)/triorb/version/drive
- Topic: (prefix)/triorb/version/pico
- Topic: (prefix)/triorb/version/core
- Type: std_msgs/msg/String
- Note: 10秒間隔で送信される.

#### 現在の指令モードの定期送信
- Topic: (prefix)/drive/mode
- Type: std_msgs/msg/String
- Value:
    - "idle": 停止中
    - "run_vel": 速度ベクトル指示による移動中
    - "run_pos": 移動距離指示による相対移動中
    - "lift": リフター動作中
- Note: 1.5秒間隔で送信される.
- Node: [注意] モーターライフタイムタイムアウト時は"idle"に戻らない

### Service

#### 速度ベクトル指示による移動（速度到達確認あり）
- Topic: (prefix)/srv/drive/run_vel
- Type: triorb_drive_interface/srv/TriorbRunVel3
- Usage： 
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/motor/status triorb_drive_interface/srv/MotorStatus  
requester: making request: triorb_drive_interface.srv.MotorStatus_Request(request=std_msgs.msg.Empty()) 

response: 
triorb_drive_interface.srv.MotorStatus_Response(result=triorb_drive_interface.msg.MotorStatus(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1709711017, nanosec=956667335), frame_id='serial'), last_error_value=0, last_error_motor=255, voltage=0.0, state=0, power=0.0)) 
```
 
#### 移動距離指示による相対移動（移動完了確認あり）
- Topic: (prefix)/srv/drive/run_pos
- Type: triorb_drive_interface/srv/TriorbRunPos3
- Usage： 
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /srv/drive/run_pos \
triorb_drive_interface/srv/TriorbRunPos3 "{request: {speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, position: {x: 0.0, y: 1.0, deg: 0.0} }  }" 
## コマンド以上 

waiting for service to become available... 
requester: making request: 
triorb_drive_interface.srv.TriorbRunPos3_Request(request=triorb_drive_interface.msg.TriorbRunPos3(speed=triorb_drive_interface.msg.TriorbSpeed(acc=500, dec=500, xy=0.1, w=0.0), position=triorb_drive_interface.msg.TriorbPos3(x=0.0, y=1.0, deg=0.0))) 

response: 
triorb_drive_interface.srv.TriorbRunPos3_Response(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1717490931, nanosec=365277011), frame_id='serial'), result=2) 
```

#### モーターステータス取得
- Topic：(prefix)/get/motor/status
- Type： triorb_drive_interface/srv/MotorStatus
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/motor/status triorb_drive_interface/srv/MotorStatus 
requester: making request: triorb_drive_interface.srv.MotorStatus_Request(request=std_msgs.msg.Empty())

response:
triorb_drive_interface.srv.MotorStatus_Response(result=triorb_drive_interface.msg.MotorStatus(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1709711017, nanosec=956667335), frame_id='serial'), last_error_value=0, last_error_motor=255, voltage=0.0, state=0, power=0.0))
```

#### エラー履歴の取得
- Topic：(prefix)/get/error/history
- Type： triorb_static_interface/srv/ErrorList
- Note: Responseに表示されるstampはpicoが起動してから経過した時間を表しており, Jetson内のタイムスタンプとは関係がない.
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/error/history triorb_static_interface/srv/ErrorList
waiting for service to become available...
requester: making request: triorb_static_interface.srv.ErrorList_Request(request=std_msgs.msg.Empty())

response:
triorb_static_interface.srv.ErrorList_Response(errors=[triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error0'), error=0), triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error1'), error=0), triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error2'), error=0), triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error3'), error=0), triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error4'), error=0)])
```

#### 励磁オン
- Topic: (prefix)/srv/drive/wakeup
- Type: std_srvs/srv/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 service call /srv/drive/wakeup std_srvs/srv/Empty
```

#### 励磁オフ
- Topic: (prefix)/srv/drive/sleep
- Type: std_srvs/srv/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 service call /srv/drive/sleep std_srvs/srv/Empty
```

## Package: triorb_dead_reckoning
### Package Description
- IMU・オドメトリ・VSLAMデータを統合し、iSAM2グラフ最適化を用いたデッドレコニングによる自己位置推定を行うROS2ノードです。推定結果はトピック配信、デバッグモードでCSVログの出力をします。

### Subscriber
#### オドメトリデータを受信して自己位置推定に利用
- Topic: (prefix)/triorb/odom
- Type: geometry_msgs/msg/Vector3Stamped

#### VSLAM推定姿勢データを受信して自己位置推定に利用
- Topic: (prefix)/vslam/rig_tf
- Type: geometry_msgs/msg/TransformStamped

### Publisher
#### デッドレコニング推定結果を配信
- Topic: (prefix)/triorb/dead_reckoning
- Type: geometry_msgs/msg/Vector3Stamped

#### ノードの動作開始通知
- Topic: (prefix)/_{ノード名}
Type: std_msgs/msg/Empty

### Service
#### ノードのバージョン情報を取得
- Topic: (prefix)/get/version/{ノード名}
- Type: triorb_static_interface/srv/Version

### Action
本パッケージではActionは利用していません。

### MQTT
#### id
- triorb_dead_reckoning_stream_{random.randint(0, 10000)}
#### Publish
- Topic: /dead_reckoning/stream
    - jeson format
    ```bash
    {
    "imu_acc":[x,x,z]
    "imu_gyro":[x,x,z]
    "odometry":[x,x,w]
    "vslam":[x,x,w]
    "gtsam":[x,x,w]
    "serial_status":"状態をstring"
    "vslam_off":"状態をTrue/False"
    }
    ```
#### Subscribe
- Topic: /dead_reckoning/debug/start
    - デバッグモード開始 Emptyメッセージ
- Topic: /dead_reckoning/debug/end
    - デバッグモード終了 Emptyメッセージ
- Topic: /dead_reckoning/vslam/off
    - vslam/rig_tfを無視 Emptyメッセージ

## Package: triorb_vslam_tf
VSLAMで計算された姿勢をTriOrbで使用するための姿勢に変換し, tf2 bufferにbroadcastするパッケージ. <br>
変換した姿勢はロボットコントローラ上での表示や, 自律移動の際の現在位置として利用される. <br>

### 主な機能
- ロボット姿勢(VSLAM座標系)をTriOrb座標系に変換
- ロボット姿勢をtf2 bufferにbroadcast

### 更新履歴
#### 1.1.0
- tf_broadcast時の robot および rig にprefixを追加
  - ROS_LOCALHOST_ONLY=0のロボットが複数いる場合に別ロボットの姿勢を参照することがある問題の対策のため

### Subscriber
#### ロボット姿勢(VSLAM座標系)を取得
- Topic: (prefix)/run_slam/camera_pose
- Type: nav_msgs/msg/Odometry

### Publisher
#### ロボット現在位置 
- Topic: (prefix)/vslam/rig_tf
- Type: geometry_msgs/msg/TransformStamped
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 topic echo --once /vslam/rig_tf 
header: 
  stamp: 
    sec: 1715249621 
    nanosec: 829307689 
  frame_id: triorb_map 
child_frame_id: robot 
transform: 
  translation: 
    x: 0.20051919812047725 
    y: -0.10789784916572422 
    z: -0.11166990297891966 
  rotation: 
    x: -0.0017948546889115379 
    y: -0.006014784536615234 
    z: 0.005654869190860537 
    w: 0.9999643110221774
```

#### ロボット現在位置（平面内）
- Topic: (prefix)/vslam/robot_pose
- Type: triorb_drive_interface/msg/TriorbPos3
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 topic echo --once /vslam/robot_pose
x: 0.06437481194734573
y: 0.05932913348078728
deg: 4.468038082122803
```


## Package: triorb_navigation

### 更新履歴
#### 1.2.1
- 自律移動の状態通知用のトピックを追加
 - 1秒周期で通知する

#### 1.2.0
- forceのモード追加. 
    - レーン維持モード追加
- Jetson内に保存された最低速度と最高速度(triorb_drive_picoでpicoから取得)を反映.
- 斜め方向並進移動で最高速度を越えないように修正.

#### 1.1.0
- forceのモード追加. bitフラグで指定できるように変更.
    - 回転のみモード追加
    - 並進のみモード追加
    - 速度指示モード追加(要調整)
    - 事後フィードバック制御モード追加
- 無フィードバック制御版が必ず失敗になっていたバグ修正
- 速度指示用のPIDパラメータ追加
- lookup_transformの参照先(robot)にprefixを追加
  - ROS_LOCALHOST_ONLY=0のロボットが複数いる場合に別ロボットの姿勢を参照することがある問題の対策のため
- 速度指示モードではlifetimeを設定


### 動作モード(forceフラグ)
各bitの組合せで指定
- フィードバック制御フラグ(0b00000001)
    - 0でフィードバック制御しない
    - 1でフィードバック制御する
    - 速度指示モードと事後フィードバック制御モードでは無効
- 事後フィードバック制御フラグ(0b00000010)
    - フィードバック制御しない場合、移動完了後にフィードバック制御を行う
    - おおまかに位置決めした後に精密位置合わせしたい場合に使用
- 回転モードフラグ(0b00001000)
    - 並進指示値が常に0になり、並進方向の精度を無視する
    - 並進モードフラグと併用できない（移動しないが常に成功判定になる）
- レーン維持モード(0b00010000)
    - 速度指示モードと同時に使用する(0b10010000)。
    - 経由点間を結ぶ直線に沿って移動する。
    - 回転を伴う移動中は、均等に回転させる。
- 並進モードフラグ(0b00010000)
    - 回転指示値が常に0になり、回転方向の精度を無視する
    - 何らかの原因でロボットが回転した場合でも元の角度に復帰することはない
    - 回転モードフラグと併用すると正常に動作しない
- 速度指示モード(0b10000000)
    - 速度指示モードになり、見た目上なめらかに動く
    - フィードバック制御フラグに関わらずフィードバック制御を行う

### 自律移動状態(state変数)
- 待機中(state=0)
  - 自律移動指示を一度も受け取っていない
  - /drive/stopトピックにより、自律移動が終了した
- 自律移動中(state=1)
  - 自律移動指示を受け移動中
- 中断(state=2)
  - /drive/pauseトピックにより、自律移動が中断した
- 成功終了(state=3)
  - 目標地点に到達した
  - ロボットがゴール地点から離れると、state=5に遷移する
- 失敗終了(state=4)
  - 目標地点に到達できなかった
  - force=0を除き、自己位置認識できないことが原因
- 目標地点から離脱(state=5)
  - 成功終了後、何らかの移動指示により目標地点から離れた


### Subscriber
#### 自律移動を終了する
- Topic: (prefix)/drive/stop
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/stop std_msgs/msg/Empty 
```

#### 世界座標系目標位置指示による移動 
- Topic: (prefix)/drive/set_pos
- Type: triorb_drive_interface/msg/TriorbSetPos3
- Usage: 
```bash
```
#### 自律移動時のPIDゲインを設定する
- Topic: (prefix)/setting/drive/gains
- Type: triorb_drive_interface/msg/DriveGains
- Usage: 
```bash
```

### Publisher
#### 移動距離指示による相対移動
- Topic: (prefix)/drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage: 
```bash
```
#### 自律移動完結果
- Topic: (prefix)/drive/result
- Type: triorb_drive_interface/msg/TriorbRunResult
- Usage: 
```bash
```

#### 自律移動状態
- Topic: (prefix)/drive/state
- Type: triorb_drive_interface/msg/TriorbRunState
- Usage: 
```bash
```

### Service
#### 世界座標系目標位置指示による移動（移動完了結果報告あり） 
- Topic: (prefix)/srv/drive/set_pos
- Type: triorb_drive_interface/srv/TriorbSetPos3
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /srv/drive/set_pos \ 
triorb_drive_interface/srv/TriorbSetPos3 "{pos: { setting: { tx: 0.01, ty: 0.01, tr: 1.0, force: 1} , pos: {speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, position: {x: 0.6037, y: 0.3599, deg: 0.3176}}}}" 
## コマンド以上 

waiting for service to become available... 
requester: making request: 
triorb_drive_interface.srv.TriorbSetPos3_Request(pos=triorb_drive_interface.msg.TriorbSetPos3(pos=triorb_drive_interface.msg.TriorbRunPos3(speed=triorb_drive_interface.msg.TriorbSpeed(acc=500, dec=500, xy=0.1, w=0.0), position=triorb_drive_interface.msg.TriorbPos3(x=0.6037, y=0.3599, deg=0.3176)), setting=triorb_drive_interface.msg.TriorbRunSetting(tx=0.01, ty=0.01, tr=1.0, force=1))) 

response: 
triorb_drive_interface.srv.TriorbSetPos3_Response(result=triorb_drive_interface.msg.TriorbRunResult(success=True, position=triorb_drive_interface.msg.TriorbPos3(x=0.5981971025466919, y=0.3542609214782715, deg=0.3284424841403961)))
```

### Action
#### 世界座標系目標経路指示による移動（途中経過、移動完了結果報告あり） 
- Topic: (prefix)/action/drive/set_path
- Type: triorb_drive_interface/action/TriorbSetPath
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 action send_goal /action/drive/set_path \ 
triorb_drive_interface/action/TriorbSetPath "{path: \ 
  [ \ 
    { \ 
      setting: {tx: 0.01, ty: 0.01, tr: 1.0, force: 1}, \ 
      pos: { \ 
        speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, \ 
        position: {x: 0.6033, y: 0.3756, deg: 0.3506} \ 
      } \ 
    }, \ 
    { \ 
      setting: {tx: 0.01, ty: 0.01, tr: 1.0, force: 1}, \ 
      pos: { \ 
        speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, \ 
        position: {x: 0.2765, y: -0.3236, deg: 0.7407} \ 
      } \ 
    }, \ 
    { \ 
      setting: {tx: 0.01, ty: 0.01, tr: 1.0, force: 1}, \ 
      pos: { \ 
        speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, \ 
        position: {x: 0.6033, y: 0.3756, deg: 0.3506} \ 
      } \ 
    } \ 
  ] \ 
}" --feedback 
## コマンド以上 

Goal accepted with ID: cd019fbfa70349789c87ea90fdd10239 

Feedback: 
    way_idx: 0 
now: 
  x: 0.6081861257553101 
  y: 0.38933515548706055 
  deg: 0.1585390269756317 
## ---- (フィードバック略) ---- 

Feedback: 
    way_idx: 2 
now: 
  x: 0.5898382663726807 
  y: 0.35128170251846313 
  deg: -0.009930066764354706 

Result: 
    result: 
  success: true 
  position: 
    x: 0.5965888500213623 
    y: 0.3684644103050232 
    deg: 0.07557345926761627 

Goal finished with status: SUCCEEDED 
```


## triorb_safe_run_cpp

C++ implementation of TriOrb's safe run-velocity filter node. The node synchronizes SICK point cloud streams, builds a lightweight occupancy map, and publishes safer `/drive/run_vel` commands derived from `/safe_drive/run_vel` by means of a potential-field based repulsive force model.

### Node interface
| Direction | Topic | Type | Notes |
|-----------|-------|------|-------|
| Subscribe | `/<prefix>/sick/point2d/right` (configurable) | `sensor_msgs/msg/PointCloud` | Synchronized via ApproximateTime. `point2d_topics` can list two or more streams. |
| Subscribe | `/<prefix>/sick/point2d/left` (configurable) | `sensor_msgs/msg/PointCloud` | Same as above; add entries in config to change topics. |
| Subscribe | `/<prefix>/safe_drive/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3` | Raw velocity command to be filtered. |
| Publish   | `/<prefix>/drive/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3` | Safe velocity command after potential-field filtering. |
| Publish   | `/<prefix>/drive/set_life_time` | `std_msgs/msg/UInt16` | Optional watchdog lifetime (currently throttled). |
| Publish   | `/<prefix>/triorb_safe_run/debug/image/compressed` | `sensor_msgs/msg/CompressedImage` | Enabled when `enable_image_pub=true`; shows occupancy & vectors. |
| Publish   | `/<prefix>/except_handl/node/add` etc. | `std_msgs/msg/String` | Registration and diagnostic topics inherited from Python node. |
| Service   | `/<prefix>/triorb_safe_run/set_config` | `triorb_static_interface/srv/SetString` | Pass a JSON string (first element of `request[]`) to replace the runtime configuration. |
| Service   | `/<prefix>/triorb_safe_run/get_config` | `triorb_static_interface/srv/GetString` | Returns the current configuration as JSON text in `result`. |

Prefix depends on `ROS_PREFIX` env var (same mechanic as Python版) to allow namespace scoping.

### Repository layout
- `include/triorb_safe_run_cpp/` – public headers (`safe_run_node.hpp`).
- `src/` – node implementation (`safe_run_node.cpp`).
- `config/` – sample parameter files (copy `sample_config.json` and adjust per robot).
- `launch/` – placeholder for future launch files.

### Key features
- ApproximateTime synchronized `sensor_msgs::msg::PointCloud` subscribers.
- Occupancy map persistence with optional decay (`map_decay`).
- Angle-weighted potential forces with velocity bias (`velocity_bias`) to keep repulsion even when vehicle speeds are low.
- Safety controller that blends filtered velocity commands and republishes `/drive/run_vel`.
- Optional debug compressed image publisher (`enable_image_pub`).

### Building
```bash
colcon build --packages-select triorb_safe_run_cpp
source install/setup.bash
```

### Running
```bash
ros2 run triorb_safe_run_cpp safe_run_cpp_node --ros-args -p config_file:=/path/to/your_config.json
##ros2 run triorb_safe_run_cpp safe_run_cpp_node --ros-args -p config_file:=/ws/pkgs/triorb_drive/triorb_safe_run_cpp/config/sample_config.json
```
Common parameters (see `config/sample_config.json` for full list):
- `point2d_topics`: array of SICK point cloud topics.
- `point2d_topics_csv`: same as上記だがカンマ区切り文字列で指定したいときに使用 (`topic_a,topic_b,...`)。
- `anker_points`: footprint vertices used for potential anchor calculations (mm units).
- `anker_points_csv`: `x0,y0,x1,y1,...` 形式でアンカーポイントを一括指定。
- `force_coeff_linear`, `watch_angle_coeff`, `velocity_bias`: tune repulsive force behavior.
- `map_decay`: 0.0–1.0 blend factor to retain past obstacles.
- `ctrl_ms`, `vel_decay_coeff`, `vel_filter_weight`: control loop cadence and smoothing.

### Notes / Best practices
1. Ensure all `point2d_topics` publishers are available before launching; the node waits but exits if none are provided in the config.
2. Disable `map_decay` (set to 0) if you require instantaneous obstacle clearing; otherwise a small decay (e.g., 0.4) stabilizes noisy scans.
3. `watch_angle_coeff` compresses or widens the effective FOV of repulsion; smaller values help catch side obstacles.
4. When tuning, start with `velocity_bias = 0.0` and increase only if you need residual repulsion when nearly stopped.
5. For visualization, set `enable_image_pub=true` and inspect `/triorb_safe_run/debug/image/compressed`.

Contributions: please keep the README/Agent files updated as parameters or behavior change.


## Package: triorb_drive_vector

### Description
- 制御指令値からロボットの進行方向や停止・回転などの状態判定を行う。SLSやLED制御向け。
- 閾値設定はdrive_vector.xml

### Subscriber
#### 移動指令を取得
- Topic: /drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage:
```bash
ros2 topic pub --once /drive/run_pos triorb_drive_interface/msg/TriorbRunPos3 \
  '{position: {x: 0.1, y: 0.0, deg: 0.0}, speed: {acc: 300, dec: 300, xy: 0.2, w: 0.0}}'
```

#### 移動指令を取得
- Topic: /drive/run_vel
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage:
```bash
ros2 topic pub --once /drive/run_vel triorb_drive_interface/msg/TriorbRunPos3 \
  '{position: {x: 0.0, y: 0.0, deg: 0.0}, speed: {acc: 0, dec: 0, xy: 0.0, w: 0.6}}'
```

### Publisher
#### 移動方向
- Topic: /drive/std_vector
- Type: Float32MultiArray
  - 配列フォーマット
  ```bash
  direction: 方向
  speed: 速度
  f_rotate: 時計回り 1 / 反時計回り -1
  f_stop: 停止と判定した際 1 / その他 -1
  ```
  - 例: 直進で停止判定なし
  ```bash
  ros2 topic echo --once /drive/std_vector
  data: [1.57, 0.35, -1.0, -1.0]
  ```
#### 移動方向2
- Topic: /drive/std_vector2
- Type: Float32MultiArray
  - 配列フォーマット
  ```bash
  direction: 並進方向 [deg] （-180～180. 正面が0, 右方向が正.）
  speed: 並進速度 [m/s]
  vw: 回転角速度 [rad/s] (CW: +, CCW: -)
  ```

#### ノードの動作開始通知
- Topic: (prefix)/_{ノード名}
- Type: std_msgs/msg/Empty
 - Usage:
```bash
ros2 topic echo --once /_triorb_drive_vector
```

### Service
#### ノードのバージョン情報を取得
- Topic: (prefix)/get/version/{ノード名}
- Type: triorb_static_interface/srv/Version
 - Usage:
```bash
ros2 service call /get/version/triorb_drive_vector triorb_static_interface/srv/Version {}
```

### Action
本パッケージではActionは利用していません。

## Package: triorb_tagslam_manager

### 概要
TriOrb製Tagslamシステムの運用をまとめて管理するROS 2ノードです。地図保存/読み込みの指示に応じて`tagslam`や`sync_and_detect`ノードをtmuxセッションで再起動し、地図ファイルの生成・差し替え、状態通知、tf配信、Version応答までを一括で行います。`ROS_PREFIX`環境変数で名前空間を付与しており、同じプレフィックスを持つトピック/サービスへ自動でリマップされます。

### ノード実行
```bash
ros2 run triorb_tagslam_manager tagslam_manager_node
```
`UNIQUE_NODE=True`のため、同名ノードが既に起動していると即座に終了します。内部では`/params/tagslam`配下の設定ファイルや`/data/tagslam_map`配下の地図を参照/更新します。

### パラメータ
| 名前 | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `use_approx_sync` | bool | `True` | `tagslam`/`sync_and_detect`を起動する際に約同期を有効にするかどうか。 |
| `replace_noise` | bool | `True` | 地図読込時に`position_noise`/`rotation_noise`を`1e-8`へ書き換えてタグ姿勢を固定するかどうか。 |

### Subscriber（外部からの呼び出し例付き）
各トピック名は`ROS_PREFIX`が設定されていれば`/<prefix>/...`に変換されます。以下のコマンド例では`ROS_PREFIX=/robot`を想定しています。

#### `/tagslam/save/map` (`std_msgs/msg/String`)
- 地図保存要求。msg.dataを地図ディレクトリ名として`/data/tagslam_map/<名前>`に保存します。`/`は`_`に置換されます。
- 外部送信例:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/tagslam/save/map std_msgs/msg/String '{data: "warehouse_202405"}'
  ```

#### `/tagslam/load/map` (`std_msgs/msg/String`)
- JSONまたは単純文字列で地図操作モードを受付けます。`mode`により動作が変わります。
  - `load`: 既存地図を読み込み、`tagslam`/`sync_and_detect`を再起動。`is_static`(bool)、`slow_mode`(bool)、`amnesia`(bool)、`map_name`(string)を指定。
  - `initialize`: `/params/tagslam/tagslam_original.yaml`を元に初期タグ情報を生成し直して再起動。後述のパラメータを任意指定可能。
  - `remove`: `map_name`配下の保存済み地図を削除。
- 外部送信例（地図読込）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/tagslam/load/map std_msgs/msg/String \
    "{data: '{\"mode\":\"load\",\"map_name\":\"warehouse_202405\",\"is_static\":true,\"slow_mode\":false,\"amnesia\":true}'}"
  ```
- 外部送信例（初期化）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/tagslam/load/map std_msgs/msg/String \
    "{data: '{\"mode\":\"initialize\",\"origin_tag_id\":1,\"origin_tag_size\":150,\"origin_tag_pos_z\":0,\"origin_tag_pos_deg\":0,\"default_tag_size\":120,\"optimizer_mode\":\"fast\"}'}"
  ```
- 外部送信例（削除）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/tagslam/load/map std_msgs/msg/String \
    "{data: '{\"mode\":\"remove\",\"map_name\":\"warehouse_202405\"}'}"
  ```

#### `/odom/body_t_rig` (`nav_msgs/msg/Odometry`)
- ボディ座標系に対するリグ座標系のOdometry。受信すると`/tagslam/rig_tf`へ`TransformStamped`として流し、SLAMロスト判定用のタイマも更新します。
- 外部送信例（静的姿勢を一度だけ送る）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/odom/body_t_rig nav_msgs/msg/Odometry \
    '{pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 1.0, x: 0.0, y: 0.0, z: 0.0}}}}'
  ```

#### `cameras[*].tag_topic` (`apriltag_msgs/msg/AprilTagDetectionArray`)
- `/params/tagslam/cameras.yaml`に記述された全カメラの`tag_topic`へ動的にSubscriberを張り、検出中タグIDを追跡します。`set_tag_size_from_file`で読みだしたサイズと合わせて`/tagslam/tag_tf`のメタ情報として利用されます。
- 外部送信例（例: `/robot/camera0/detector/tags`へダミー配信）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/camera0/detector/tags apriltag_msgs/msg/AprilTagDetectionArray \
    '{detections: [{id: 100}]}' 
  ```

### Publisher
| Topic | 型 | 内容 |
| --- | --- | --- |
| `/tagslam/rig_tf` | `geometry_msgs/msg/TransformStamped` | `/odom/body_t_rig`で受信した姿勢をTF互換形式に変換。 |
| `/tagslam/tag_tf` | `geometry_msgs/msg/TransformStamped` | `tf_buffer`に存在するタグ姿勢を周期送信。`header.frame_id`にはタグサイズ、`child_frame_id`の末尾には`look`/`known`を追記。 |
| `/tagslam/state` | `std_msgs/msg/UInt8MultiArray` | `StateCode`（WORKING/SAVE_MAP/LOAD_MAP）の進捗。`StateValue`(0:STANDBY,1:PROCESSING,2:SUCCESS,3:LOST)または`64+ErrorValue`を格納。 |
| `/tagslam/map_name` | `std_msgs/msg/String` | 現在ロード済みの地図名。 |
| `/tagslam/status` | `triorb_slam_interface/msg/SlamStatus` | ビットフラグでSLAM状態/エラーを通知。state: bit0=FIXマップ、bit1=ローカライズ成功、bit2=保存処理中、bit3=読込処理中。error: bit0=tagslam停止、bit1=既知タグ未検出、bit2=保存失敗、bit3=読込失敗。 |

### Service
| Service | 型 | 説明 |
| --- | --- | --- |
| `/get/version/tagslam_manager_node` | `triorb_static_interface/srv/Version` | ノードバージョン(現在`0.0.0`)を返却。`ROS_PREFIX`が付与された名前空間に配置されます。 |

### 地図操作の詳細
- **保存**: `/tagslam/save/map`受信後`/dump`サービス(Trigger)を呼び出し、`poses.yaml`と`camera_poses.yaml`を取得。`tagslam.yaml`の`bodies`以降を`poses.yaml`で置き換え、`/data/tagslam_map/<name>/tagslam_map.yaml`に書き出します。完了/エラーを`/tagslam/state`および`/tagslam/status`で通知。
- **読込**: `/tagslam/load/map`で`mode=load`を受けると、保存済み地図を`/params/tagslam/target_map.yaml`へ複写しながら`is_static`指定やノイズ置換を実施。完了後`tmux`セッション`detect`と`tagslam`を再起動し、tfバッファをリセットしてタグサイズ辞書を再生成します。
- **初期化**: `mode=initialize`では`tagslam_original.yaml`を基にタグID/サイズ/高さ/姿勢/デフォルトサイズ、`optimizer_mode`(`fast|slow|full`)、`minimum_viewing_angle`、`minimum_tag_area`などを上書きして`tagslam.yaml`を生成。再起動後は地図名を空にします。
- **削除**: `mode=remove`では`/data/tagslam_map/<map_name>`を再帰的に削除します。

### 状態監視
- `check_state()`が1秒周期で`tagslam`/`sync_and_detect`ノードの生存確認とロスト判定（2秒以内に`/odom/body_t_rig`更新が無い場合は`LOST`）を行い、`/tagslam/state`と`/tagslam/status`へ反映します。
- `check_tf_tree()`が1秒周期で`tf_buffer`から既知タグ一覧を取得し、`/tagslam/tag_tf`に送出します。
- `check_srv_call_result()`が地図保存のサービス応答を監視し、`ErrorValue`（BUSY/ TIMEOUT/ NOT_FOUND/ UNKNOWN）を付与します。

### カメラ設定の扱い
起動時に`/params/tagslam/cameras.yaml`を読み込み、`ROS_PREFIX`付きトピックへ書き換えた結果を`/params/tagslam/cameras_prefix.yaml`（既定`cameras_prefix.yaml`）として保存します。同時にカメラ検出トピックへSubscriberを張り、`detector_callback`で検出タグを記録することで、タグTFメッセージに「現在視認中か既知のみか」を付加します。

### 補足
- `tmux kill-session -t tagslam|detect`で既存セッションを切り替える設計のため、同名セッションを他用途で使わないでください。
- `/params`および`/data`パスはDockerコンテナなどでボリュームマウントされている前提です。必要に応じてシンボリックリンクで実ファイルを差し替えてください。


## Package: stella_vslam_ros

このドキュメントは、`/run_slam` ノードにおける ROS2 Publish / Subscribe トピックの一覧を示します。

---

### 🔄 Publish トピック一覧

| トピック名 | メッセージ型 | 説明 |
|------------|---------------|------|
| `/run_slam/camera_pose` | `nav_msgs::msg::Odometry` | 推定されたカメラ姿勢 |
| `/run_slam/keyframes` | `geometry_msgs::msg::PoseArray` | キーフレーム群 |
| `/run_slam/keyframes_2d` | `geometry_msgs::msg::PoseArray` | 平面に投影されたキーフレーム |
| `/run_slam/pose_2d` | `geometry_msgs::msg::Pose2D` | 2D平面上のカメラ姿勢 |
| `/run_slam/keyframe_landmarks` | `triorb_slam_interface::msg::UInt32MultiArrayStamped` | キーフレームごとのランドマーク数 |
| `/run_slam/matched_landmarks` | `triorb_slam_interface::msg::UInt32MultiArrayStamped` | マッチしたランドマーク数 |
| `/run_slam/matched_points` | `triorb_slam_interface::msg::PointArrayStamped` | マッチした3D点群 |
| `/run_slam/camera_pose_dev` | `triorb_slam_interface::msg::PoseDevStamped` | カメラ姿勢推定結果（validフラグ付き） |
| `/run_slam/matched_landmarks_per_camera` | `triorb_slam_interface::msg::CamerasLandmarkInfo` | カメラごとのランドマーク情報 |
| `/run_slam/cameras_pose` | `triorb_slam_interface::msg::CamerasPose` | 複数カメラの姿勢 |
| `/run_slam/enable_camera` | `std_msgs::msg::Int8MultiArray` | 使用カメラの有効/無効状態 |
| `/run_slam/marker_only` | `std_msgs::msg::Bool` | マーカーのみを使うか |
| `/run_slam/marker_exclude` | `std_msgs::msg::Bool` | マーカー領域の除外フラグ |
| `/run_slam/map_file_path` | `std_msgs::msg::String` | 現在のマップファイルパス |
| `/run_slam/map_file_changed` | `std_msgs::msg::String` | マップファイル変更通知 |
| `/run_slam/local_map_file_path` | `std_msgs::msg::String` | ローカルマップファイルパス |
| `/run_slam/current_keyframes` | `triorb_slam_interface::msg::KeyframeArray` | 現在のキーフレーム情報 |
| `/run_slam/map_freeze` | `std_msgs::msg::Bool` | 地図固定モードの状態 |
| `/except_handl/node/add` | `std_msgs::msg::String` | 例外発生ノード通知 |
| `/triorb/error/str/add` | `std_msgs::msg::String` | エラーメッセージ通知 |
| `/triorb/warn/str/add` | `std_msgs::msg::String` | ワーニング通知 |

---

### 📥 Subscribe トピック一覧

| トピック名 | メッセージ型 | 説明 |
|------------|---------------|------|
| `/run_slam/set/enable_camera` | `std_msgs::msg::Int8MultiArray` | 使用カメラ切り替え |
| `/run_slam/set/mask_positive` | `triorb_slam_interface::msg::XyArrayStamped` | 特徴点マスク（許容） |
| `/run_slam/set/mask_negative` | `triorb_slam_interface::msg::XyArrayStamped` | 特徴点マスク（除外） |
| `/run_slam/set/clear_mask_all` | `std_msgs::msg::Empty` | マスク初期化 |
| `/run_slam/set/save_mask_to_yaml` | `std_msgs::msg::Empty` | マスクYAML保存指示 |
| `/run_slam/set/marker_only` | `std_msgs::msg::Bool` | マーカーのみ利用設定 |
| `/run_slam/set/marker_exclude` | `std_msgs::msg::Bool` | マーカー領域除外設定 |
| `/run_slam/set/change_map_file_path` | `std_msgs::msg::String` | 地図ファイル変更指示 |
| `/run_slam/set/enter_local_map_file_path` | `std_msgs::msg::String` | ローカル地図ファイル切替 |
| `/run_slam/set/map_freeze` | `std_msgs::msg::Bool` | 地図固定切替 |
| `/run_slam/set/manual_keyframes` | `triorb_slam_interface::msg::KeyframeArray` | 手動リローカライズ要求 |
| `/triorb/odom` | `geometry_msgs::msg::Vector3Stamped` | オドメトリ情報（Odomono/OdoRig） |


## Package: triorb_rmf_bridge

### Description
- 単体自律移動のFMS用Topicのバイパスを行う。
- ROS_LOCALHOST_ONLY=0と1のブリッジも担うため、global/local両方のコンテナで本パッケージを起動する必要がある。
- ブリッジ対象のtopicがglobal⇔localで無限ループする可能性がある場合は"RecentNSet<std::size_t>"を使った防御を行うこと。
- Global（FMS/上位管理システム）とLocal（ロボット）を跨いで送受信されるメッセージがあるとき、Global側のTopic名は末尾にHash値が付加されたメッセージを使う
```bash
    # Global（上位管理システム）側から見たメッセージ定義：
    Topic：(prefix)/drive/run_vel
    Type：triorb_drive_interface/msg/TriorbRunVel3
    # Local（ロボット）側から見たメッセージ定義：
    Topic：(prefix)/drive/run_vel
    Type：triorb_drive_interface/msg/TriorbRunVel3
```


### ROS2 Bypass Global to Local Topic

#### マーカー座標系の目標位置
- Topic：(prefix)/drive/align_pos
- Type：triorb_drive_interface/msg/TriorbAlignPos3 

#### ロボット座標系の目標速度
- Topic：(prefix)/drive/run_vel
- Type：triorb_drive_interface/msg/TriorbRunVel3

#### Driving mode
- Topic：(prefix)/drive/set_mode
- Type：std_msgs/msg/String

#### リフター動作指示
- Topic：(prefix)/drive/run_lifter
- Type：std_msgs/msg/String

#### 停止指示
- Topic：(prefix)/drive/stop
- Type：std_msgs/msg/Empty

#### ロボット座標系の目標位置
- Topic：(prefix)/drive/run_pos
- Type：triorb_drive_interface/msg/TriorbRunPos3

#### アライメント開始
- Topic：(prefix)/drive/alignment/start
- Type：std_msgs/msg/String

#### アライメント終了
- Topic：(prefix)/drive/alignment/terminate
- Type：std_msgs/msg/String

#### FMS用watchdog
- Topic：(prefix)/fms_watchdog
- Type：std_msgs/msg/Int32

#### 世界座標系の位置・姿勢へ向かう移動実行
- Topic：(prefix)/fms/set_pos
- Type：triorb_drive_interface/msg/TriorbSetPos3

#### ロボットアームタスクの指令用
- Topic：(prefix)/arm_task_list
- Type：std_msgs/msg/String

#### 拡張基盤用発進音声トピック
- Topic：(prefix)/ext_pico/start_auto_move
- Type：std_msgs/msg/Empty

#### 拡張基盤用停止トピック
- Topic：(prefix)/ext_pico/end_auto_move
- Type：std_msgs/msg/Empty


### ROS2 Bypass Local to Global Topic

#### 世界座標系の位置・姿勢
- Topic：(prefix)/vslam/rig_tf
- Type：geometry_msgs/msg/TransformStamped

#### リフターState
- Topic：(prefix)/lifter/state
- std_msgs/msg/String

#### リフターリザルト
- Topic：(prefix)/lifter/result
- std_msgs/msg/String

#### 相対位置決めステータス配信
- Topic: (prefix)/drive/alignment/status
- Type: std_msgs/msg/String

#### 相対位置決め結果配信
- Topic: (prefix)/drive/alignment/result
- Type: std_msgs/msg/String

#### 自律移動完了結果配信
- Topic: (prefix)/drive/result
- Type: triorb_drive_interface/msg/TriorbRunResult

#### ロボットウォッチドッグ配信
- Topic: (prefix)/amr_robot_watchdog
- Type: std_msgs/msg/String

#### ロボットステータス配信
- Topic: (prefix)/robot/status
- Type: triorb_static_interface/msg/RobotStatus

#### ホストステータス配信
- Topic: (prefix)/host/status
- Type: triorb_static_interface/msg/HostStatus

## パラメーター
- BRIDGE_IP : Global ⇔ Local ブリッジに使うIPアドレス（recommend: 127.0.0.1）
- BRIDGE_PORT_G2L : Global ⇒ Local ブリッジに使うポート (default 60000)
- BRIDGE_PORT_L2G : Global ⇒ Local ブリッジに使うポート (default 60001)

## Package: triorb_except_handl
### Config
#### config/node_check.json
- node_list: 存在しない場合ERRORとするnode名を記入(string)
    - /except_handl/node/add トピックから追記可能
    - /except_handl/node/remove トピックから削除可能
- delay_sec: Node監視の開始遅延時間(float)[s]

#### config/${node_name}_restart.sh
nodeが存在しなかった場合にホスト側で実行するshell script

### Subscriber
#### エラーの受取り
- Topic: (prefix)/triorb/error/add
- Type: std_msgs::msg::UInt16
- Usage:
```bash
ros2 topic pub --once /triorb/error/add std_msgs/msg/UInt16 '{"data":49}'
```

#### エラーの受取り（任意文字列版）
- Topic: (prefix)/triorb/error/str/add
- Type: std_msgs::msg::String
- Usage:
```bash
ros2 topic pub --once /triorb/error/str/add std_msgs/msg/String '{"data": "Sample error message"}'
```

#### 警告の受取り
- Topic: (prefix)/triorb/warn/add
- Type: std_msgs::msg::UInt16
- Usage:
```bash
ros2 topic pub --once /triorb/warn/add std_msgs/msg/UInt16 '{"data":1}'
```

#### 警告の受取り（任意文字列版）
- Topic: (prefix)/triorb/warn/str/add
- Type: std_msgs::msg::String
- Usage:
```bash
ros2 topic pub --once /triorb/warn/str/add std_msgs/msg/String '{"data": "Sample warning message"}'
```

#### エラーリセットの実行
- Topic: (prefix)/triorb/error/reset
- Type: std_msgs/msg/Uint8
- Usage: 
```bash
ros2 topic pub --once /triorb/error/reset std_msgs/msg/UInt8 '{"data":1}' # dataが1以上のときリセット実行
```

#### 監視対象ノード追加
- Topic: (prefix)/except_handl/node/add
- Type: std_msgs/msg/String
- Usage: 
```bash
ros2 topic pub --once /except_handl/node/add std_msgs/msg/String '{"data":"sample_node"}'
```

#### 監視対象ノード削除
- Topic: (prefix)/except_handl/node/remove
- Type: std_msgs/msg/String
- Usage: 
```bash
ros2 topic pub --once /except_handl/node/remove std_msgs/msg/String '{"data":"sample_node"}'
```

### Publisher
#### エラー履歴の発行
- Topic: (prefix)/triorb/error/log
- Type: std_msgs::msg::UInt16MultiArray
 - 例:
```bash
ros2 topic echo --once /triorb/error/log
data:
- 32
- 49
```

#### エラー履歴の発行（文字列版）
- Topic: (prefix)/triorb/error/str/log
- Type: std_msgs::msg::String
- Format: 1件1行の平文
 - 例:
```bash
ros2 topic echo --once /triorb/error/str/log
data: "sensor timeout"
```

#### 警告履歴の発行
- Topic: (prefix)/triorb/warn/log
- Type: std_msgs::msg::UInt16MultiArray
 - 例:
```bash
ros2 topic echo --once /triorb/warn/log
data:
- 1
```

#### 警告履歴の発行（文字列版）
- Topic: (prefix)/triorb/warn/log
- Type: std_msgs::msg::String
- Format: 1件1行の平文
 - 例:
```bash
ros2 topic echo --once /triorb/warn/log
data: "map outdated"
```

#### エラー件数の発行
- Topic: (prefix)/triorb/error/num
- Type: std_msgs::msg::UInt8
 - 例:
```bash
ros2 topic echo --once /triorb/error/num
data: 2
```

#### 警告件数の発行
- Topic: (prefix)/triorb/warn/num
- Type: std_msgs::msg::UInt8
 - 例:
```bash
ros2 topic echo --once /triorb/warn/num
data: 1
```


