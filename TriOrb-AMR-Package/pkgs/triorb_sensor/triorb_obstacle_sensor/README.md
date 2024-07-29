# Package: triorb_obstacle_sensor

## Subscriber
### IMUセンサの再起動
- Topic: (prefix)/reboot/sensor/imu
- Type: std_msgs/msg/Empty
- Usage: 
```bash
```

### 距離センサの再起動
- Topic: (prefix)/reboot/sensor/distance
- Type: std_msgs/msg/Empty
- Usage: 
```bash
```

### 距離センサによる減速措置を開始する距離閾値の設定
- Topic: (prefix)/set/sensor/threshold
- Type: std_msgs/msg/Float32
- Note：確実に変更するために複数回の実行を推奨
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /set/sensor/threshold std_msgs/msg/Float32 "data: 0.5"
```

## Publisher
### IMUセンサ値
- Topic: (prefix)/sensor/imu
- Type: triorb_sensor_interface/msg/ImuSensor
- Frequency: 1/(0.02 - 0.04) Hz
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic echo --once /distance0
header:
  stamp:
    sec: 1709086507
    nanosec: 347647639
  frame_id: id01
distance: 1.225
confidence: 100
```
### 距離センサ値
- Topic: (prefix)/sensor/distance
- Type: triorb_sensor_interface/msg/DistanceSensor
- Frequency：1/(0.02 - 0.04) Hz
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic echo /sensor/distance
---
header:
  stamp:
    sec: 1717053814
    nanosec: 932199978
  frame_id: irFR
distance: 1.0709999799728394
confidence: 0
hfov: 13.5
vfov: 13.5
max_dist: 3.094062566757202
min_dist: 0.009999999776482582
mount_xyz:
- 0.10999999940395355
- 0.22759999334812164
- 0.11900000274181366
mount_ypr:
- 0.0
- 0.0
- 0.0
---
header:
  stamp:
    sec: 1717053814
    nanosec: 935458144
  frame_id: irR
distance: 0.3610000014305115
confidence: 0
hfov: 13.5
vfov: 13.5
max_dist: 3.3688902854919434
min_dist: 0.009999999776482582
mount_xyz:
- 0.24269999563694
- 0.03150000050663948
- 0.12200000137090683
mount_ypr:
- 90.0
- 0.0
- 0.0
---
header:
  stamp:
    sec: 1717053814
    nanosec: 935918224
  frame_id: irB
distance: 2.065999984741211
confidence: 0
hfov: 13.5
vfov: 13.5
max_dist: 3.1961989402770996
min_dist: 0.009999999776482582
mount_xyz:
- 0.07000000029802322
- 0.2680000066757202
- 0.12200000137090683
mount_ypr:
- 180.0
- 0.0
- 0.0
---
header:
  stamp:
    sec: 1717053814
    nanosec: 945622608
  frame_id: irFL
distance: 2.818000078201294
confidence: 0
hfov: 13.5
vfov: 13.5
max_dist: 3.1126694679260254
min_dist: 0.009999999776482582
mount_xyz:
- -0.10999999940395355
- 0.22759999334812164
- 0.11900000274181366
mount_ypr:
- 0.0
- 0.0
- 0.0
---
```

### センサデバイス接続エラー
- Topic: (prefix)/error/sensor
- Type: std_msgs/msg/Empty
- Usage: 
```bash
```