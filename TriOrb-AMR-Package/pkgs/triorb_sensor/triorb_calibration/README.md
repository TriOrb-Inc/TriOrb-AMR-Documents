# Package: triorb_calibration

# Active API
# カメラ内部パラメータのキャリブレーションプロセス開始 【closed beta】
- Topic：(prefix)/action/camera/calibration/internal
- Node：(prefix)_camera_calibration
- Type： triorb_sensor_interface/action/CameraCalibrationInternal
- Usage：
```
root@orin-nx-XXX:~/$ ros2 action send_goal /action/camera/calibration/internal triorb_sensor_interface/action/CameraCalibrationInternal "{rows: 11, cols: 8, spacing: 20, diameter: 12, src: '/data/dev/ken/220321/'}"
Waiting for an action server to become available...
Sending goal:
     rows: 11
cols: 8
spacing: 20.0
diameter: 12.0
src: /data/dev/ken/220321/

Goal accepted with ID: 1335f4b8b55c46509d6e7b838fd988fe

Result:
    image:
  header:
    stamp:
      sec: 0
      nanosec: 0
    frame_id: ''
  format: ''
  data: []
fx: 650.124267578125
fy: 647.412353515625
cx: 807.5310668945312
cy: 651.3446044921875
k1: 0.3168344795703888
k2: -1.5004156827926636
k3: 0.4790266454219818
k4: -0.041176315397024155
```
