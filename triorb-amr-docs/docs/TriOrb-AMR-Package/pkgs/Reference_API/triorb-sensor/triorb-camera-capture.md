# triorb_camera_capture

**パス**: `triorb_sensor/triorb_camera_capture`  
**説明**: カメラキャプチャーのためのパッケージ

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


