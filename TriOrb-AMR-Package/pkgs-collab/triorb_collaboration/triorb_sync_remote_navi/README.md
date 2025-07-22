# Package: triorb_sync_remote_navi
リモコン協調制御のためのパッケージ

# Parameter
- DISCONNECT_MS : リモコン操作されていないとみなし、速度パブリッシュを停止する時間[ms]
- SOCKET_PORT : ブラウザからSOCKET受信するポート番号
- SOCKET_IP : ブラウザからSOCKET受信するアドレス
- PUBLISH_RATE_MS : 速度ベクトルをパブリッシュする時間間隔[ms]
- ROBOT_LIST : 操作対象のロボット一覧

# Subscriber
## リモコン協調バインド開始Request
- Topic: (prefix)/collab/remote/bind/start
- Type： std_msgs/msg/String
- Usate：
```bash
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/remote/bind/start std_msgs/msg/String \
"{data : '{\
    "'"robot"'" : ["'"hostname_1"'","'"hostname_2"'"]\
}'}"
```

## リモコン協調バインド終了Request
- Topic: (prefix)/collab/remote/bind/terminate
- Type： std_msgs/msg/String
- Usate：
```bash
# robotリストは空でもよい
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/remote/bind/terminate std_msgs/msg/String \
"{data : '{\
    "'"robot"'" : ["'"hostname_1"'","'"hostname_2"'"]\
}'}"
```


## リモコン協調開始Request
- Topic: (prefix)/collab/remote/request
- Type： std_msgs/msg/String
- Usate：
```bash
# triorb_drive_interface/msg/TriorbSetPos3型相当を含んだメッセージを送信する
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/remote/request std_msgs/msg/String \
"{data : '{\
    "'"name"'" : "'"test_job_001"'",\
    "'"robot"'" : ["'"hostname_1"'","'"hostname_2"'"]\
}'}"
```

## リモコン協調中断Request
- Topic: (prefix)/collab/remote/terminate
- Type： std_msgs/msg/String

## Mutex取得のResult
- Topic：(prefix)/collab/mutex/lock_mutex/response
- Type： std_msgs/msg/String

# Publisher
## 荷物に対する速度ベクトル
- Topic: (prefix)/collab/remote/run_vel/(HASH)
- Type： std_msgs/msg/String
- Frequency：PUBLISH_RATE_MS

## リフターUP/DOWN
- Topic: (prefix)/collab/remote/run_lift/(HASH)
- Type： std_msgs/msg/String

## Sync move開始
- Topic: (prefix)/sync_move_manager/start/navi
- Type： std_msgs/msg/String

## Sync move終了
- Topic: (prefix)/sync_move_navi/stop/navi
- Type： std_msgs/msg/String

## Mutex取得のリクエスト
- Topic：(prefix)/collab/mutex/lock_mutex
- Type： std_msgs/msg/String

## Mutex解除のリクエスト
- Topic：(prefix)/collab/mutex/unlock_mutex
- Type： std_msgs/msg/String
