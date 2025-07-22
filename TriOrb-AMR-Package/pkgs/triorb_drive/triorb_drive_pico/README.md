# Package: triorb_drive_pico

## 更新履歴
### 1.2.0
- 各バージョン取得serviceを10秒に1回publishする形式に変更
- picoから最大速度・最小速度を取得し、Jetson内に保存するコードを追加
- picoからエラー履歴を取得するservice追加
- 特定の条件で速度指示を無視していたバグ修正

### 1.1.0
- nodeのバージョン取得serviceを追加（有効になるようにバグ修正）
- picoのバージョン取得serviceを追加
- triorb_coreのバージョン取得serviceを追加
- 励磁オン・オフのservice版を追加
- 速度0命令は連続でない限りスキップしない

## Subscriber

### 励磁オン
- Topic: (prefix)/drive/wakeup
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/wakeup std_msgs/msg/Empty 
```

### 励磁オフ
- Topic: (prefix)/drive/sleep
- Type: std_msgs/msg/Empty
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/sleep std_msgs/msg/Empty
```

### 速度ベクトル指示による移動
- Topic: (prefix)/drive/run_vel
- Type: triorb_drive_interface/msg/TriorbRunVel3
- Note: 前回適用された指示と比較して, 以下の条件を両方満たす場合はスキップする.
    - 0.2秒以下の間隔
    - 速度指示値velocityのx,y,wの差が0.001以下

### 移動距離指示による相対移動
- Topic: (prefix)/drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3

### モータードライバの設定変更
- Topic: (prefix)/set/motor/params
- Type: triorb_drive_interface/msg/MotorParams
- Note: 全ての値を0にすると, 出荷時の設定を書き込む.

### 移動停止
- Topic: (prefix)/drive/stop
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/stop std_msgs/msg/Empty
```

### トルク設定変更
- Topic: (prefix)/set/motor/torque
- Type: std_msgs/msg/Float32
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /set/motor/torque std_msgs/msg/Float32 "data: 100.0" # 100%
```


## Publisher

### ロボットステータスの定期送信
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

### オドメトリの定期送信
- Topic: (prefix)/triorb/odom
- Type: geometry_msgs/msg/Vector3Stamped
- Note: 0.2秒間隔で送信される.


### バージョン情報の定期送信
- Topic: (prefix)/triorb/version/drive
- Topic: (prefix)/triorb/version/pico
- Topic: (prefix)/triorb/version/core
- Type: std_msgs/msg/String
- Note: 10秒間隔で送信される.


## Service

### 速度ベクトル指示による移動（速度到達確認あり）
- Topic: (prefix)/srv/drive/run_vel
- Type: triorb_drive_interface/srv/TriorbRunVel3
- Usage： 
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/motor/status triorb_drive_interface/srv/MotorStatus  
requester: making request: triorb_drive_interface.srv.MotorStatus_Request(request=std_msgs.msg.Empty()) 

response: 
triorb_drive_interface.srv.MotorStatus_Response(result=triorb_drive_interface.msg.MotorStatus(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1709711017, nanosec=956667335), frame_id='serial'), last_error_value=0, last_error_motor=255, voltage=0.0, state=0, power=0.0)) 
```
 
### 移動距離指示による相対移動（移動完了確認あり）
- Topic: (prefix)/srv/drive/run_pos
- Type: triorb_drive_interface/srv/TriorbRunPos3
- Usage： 
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /srv/drive/run_pos \
triorb_drive_interface/srv/TriorbRunPos3 "{request: {speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, position: {x: 0.0, y: 1.0, deg: 0.0} }  }" 
# コマンド以上 

waiting for service to become available... 
requester: making request: 
triorb_drive_interface.srv.TriorbRunPos3_Request(request=triorb_drive_interface.msg.TriorbRunPos3(speed=triorb_drive_interface.msg.TriorbSpeed(acc=500, dec=500, xy=0.1, w=0.0), position=triorb_drive_interface.msg.TriorbPos3(x=0.0, y=1.0, deg=0.0))) 

response: 
triorb_drive_interface.srv.TriorbRunPos3_Response(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1717490931, nanosec=365277011), frame_id='serial'), result=2) 
```

### モーターステータス取得
- Topic：(prefix)/get/motor/status
- Type： triorb_drive_interface/srv/MotorStatus
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/motor/status triorb_drive_interface/srv/MotorStatus 
requester: making request: triorb_drive_interface.srv.MotorStatus_Request(request=std_msgs.msg.Empty())

response:
triorb_drive_interface.srv.MotorStatus_Response(result=triorb_drive_interface.msg.MotorStatus(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1709711017, nanosec=956667335), frame_id='serial'), last_error_value=0, last_error_motor=255, voltage=0.0, state=0, power=0.0))
```

### エラー履歴の取得
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