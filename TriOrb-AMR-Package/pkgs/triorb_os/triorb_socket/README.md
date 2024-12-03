# Package: triorb_socket

## Publisher
### ソケットで受信したゲームパッド信号をJoyコマンドとしてPublishする
- Topic: /broadcast/joy
- Type: sensor_msgs/msg/Joy
- Usage: 
```bash
```

### ソケットで受信したゲームパッド信号をロボット移動コマンドとしてPublishする
- Topic: (prefix)/drive/run_vel
- Type: triorb_drive_interface/msg/TriorbRunVel3
- Usage: 
```bash
```