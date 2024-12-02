# Package: triorb_map_share
- 複数台ロボットでVSLAMの地図を共有する
- トピックをトリガーとして特定のロボット内に存在する地図ファイルをsocketで取ってくる
- 地図ファイルはMAP_ROOT_DIR以下に格納されているものとする
- 地図の授受はTCP socketを使いバイナリ列で授受する
- 実データでは未テスト
- VSLAMを自動的に再起動する仕組みは未実装

## Publisher
### 現在設定されている地図ファイル情報
- Topic: (prefix)/map/latest
- Type: std_msgs/msg/String
- Frequency: 0.1Hz
- Usage: 
```bash
```

## Service
### 共有地図を用いてVSLAMを再起動する
- Topic: (prefix)/map/set_share_map_and_run
- Type: triorb_static_interface/srv/SetString
- Note: 地図ファイルに関する情報をJSON形式で受け取る
- Usage: 
```bash
root@orin-nx-4260:/ws# ros2 service call /map/set_share_map_and_run triorb_static_interface/srv/SetString "{request: {'{"'"name"'":"'"dummy_map.sqlite3"'","'"host"'":"'"192.168.21.26"'"}'}}"
```

# パラメーター
- MAP_ROOT_DIR : マップファイルの格納ディレクトリ
- MAP_SOCKET_PORT : マップ授受のためのソケットポート
