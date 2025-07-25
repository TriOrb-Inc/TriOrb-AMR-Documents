# 自律移動 API Reference v1.2.0 (2025-07-17)

## Package: triorb_navi_bridge

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

### 更新履歴
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



## Package: triorb_streaming_images

### Subscriber
#### Imageトピックを受信し配信する
- Topic: (可変)
- Type: sensor_msgs/msg/Image


#### CompressedImageトピックを受信し配信する
- Topic: (可変)
- Type: sensor_msgs/msg/CompressedImage


## Package: triorb_navigation_manager

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

## Package: triorb_drive_pico

### 更新履歴
#### 1.2.0
- 各バージョン取得serviceを10秒に1回publishする形式に変更
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
root@orin-nx-XXX:~/$ ros2 topic pub -1 /set/motor/torque std_msgs/msg/Float32 "data: 100.0" # 100%
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


### 更新履歴
#### 1.1.0
- tf_broadcast時の robot および rig にprefixを追加
  - ROS_LOCALHOST_ONLY=0のロボットが複数いる場合に別ロボットの姿勢を参照することがある問題の対策のため

### Subscriber
#### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

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

## Package: triorb_navigation

### 更新履歴
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


## Package: triorb_drive_vector

### Description
- 制御指令値からロボットの進行方向や停止・回転などの状態判定を行う。SLSやLED制御向け。
- 閾値設定はdrive_vector.xml

### Subscriber
#### 移動指令を取得
- Topic: /drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage:

#### 移動指令を取得
- Topic: /drive/run_vel
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage:

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

#### ノードの動作開始通知
- Topic: (prefix)/_{ノード名}
- Type: std_msgs/msg/Empty

### Service
#### ノードのバージョン情報を取得
- Topic: (prefix)/get/version/{ノード名}
- Type: triorb_static_interface/srv/Version

### Action
本パッケージではActionは利用していません。

## Package: triorb_tagslam_manager

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
ros2 topic pub --once /triorb/warn/add std_msgs/msg/String '{"data": "Sample warning message"}'
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

#### エラー履歴の発行（文字列版）
- Topic: (prefix)/triorb/error/str/log
- Type: std_msgs::msg::String
- Format: 1件1行の平文

#### 警告履歴の発行
- Topic: (prefix)/triorb/warn/log
- Type: std_msgs::msg::UInt16MultiArray

#### 警告履歴の発行（文字列版）
- Topic: (prefix)/triorb/warn/log
- Type: std_msgs::msg::String
- Format: 1件1行の平文

#### エラー件数の発行
- Topic: (prefix)/triorb/error/num
- Type: std_msgs::msg::UInt8

#### 警告件数の発行
- Topic: (prefix)/triorb/warn/num
- Type: std_msgs::msg::UInt8


