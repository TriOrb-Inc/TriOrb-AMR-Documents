# Package: triorb_lifter_navi
協調搬送タスクにおけるリフターを制御するパッケージ

# （上位との通信）Subscriber
## リフターを上げ下げするRequest
- Topic：(prefix)/collab/lifter/start/request
- Type：std_msgs/msg/String
- Definition：
```bash
{
    direction : up/down,
    move : [
        {
            robot : (ロボット1のHash),
        },
        {
            robot : (ロボット2のHash),
        },
    ]
}
```
- Usage：
```bash
# ===1台目の準備===
# 1台目のリフターロボを起動（電源ON）
# 以降、１台目リフターロボのbashで実行
# mutex managerを起動
tobeta@orin-nx-4260:~/TriOrb-AMR-Package-Collab$ sh run_mutex_manager.sh
# lifter navi, drive picoを起動
tobeta@orin-nx-4260:~/TriOrb-AMR-Package-Collab$ sh dev_collab_lifter.sh
# globalスコープのdockerコンテナに入る
tobeta@orin-nx-4260:~/TriOrb-AMR-Package-Collab$ docker attach dev_lifter_global
# 強制的に１台目のMutexを取得する
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/mutex/lock_mutex std_msgs/msg/String '{data: TestMutex1}' # 1台目

# ===2台目の準備===
# 2台目のリフターロボを起動（電源ON）
# 以降、2台目リフターロボのbashで実行
# mutex managerを起動
tobeta@toga-go-01:~/TriOrb-AMR-Package-Collab$ sh run_mutex_manager.sh
# lifter navi, drive picoを起動
tobeta@toga-go-01:~/TriOrb-AMR-Package-Collab$ sh dev_collab_lifter.sh
# 以降、１台目リフターロボのbashで実行
# "1台目の"globalスコープのdockerコンテナに入る
tobeta@orin-nx-4260:~/TriOrb-AMR-Package-Collab$ docker attach dev_lifter_global
# 強制的に2台目のMutexを取得する
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/mutex/lock_mutex std_msgs/msg/String '{data: TestMutex2}' # 2台目

# ===同時にリフターを上げる===
# 以降、１台目もしくは２台目のリフターロボのbashで実行
# globalスコープのdockerコンテナに入る
tobeta@orin-nx-4260:~/TriOrb-AMR-Package-Collab$ docker attach dev_lifter_global
# Lifter Naviにリフターを上げるコマンドを送信する
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/lifter/start/request std_msgs/msg/String \
"{data : '{\
    "'"direction"'" : "'"up"'",\
    "'"move"'" : \
    [\
        {\
            "'"robot"'" : "'"TestMutex1"'"\
        },\
        {\
            "'"robot"'" : "'"TestMutex2"'"\
        }\
    ]\
}'}"

# ===同時にリフターを下げる===
# 以降、１台目もしくは２台目のリフターロボのbashで実行
# globalスコープのdockerコンテナに入る
tobeta@orin-nx-4260:~/TriOrb-AMR-Package-Collab$ docker attach dev_lifter_global
# Lifter Naviにリフターを下げるコマンドを送信する
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/lifter/start/request std_msgs/msg/String \
"{data : '{\
    "'"direction"'" : "'"down"'",\
    "'"move"'" : \
    [\
        {\
            "'"robot"'" : "'"TestMutex1"'"\
        },\
        {\
            "'"robot"'" : "'"TestMutex2"'"\
        }\
    ]\
}'}"
```

# （上位との通信）Publisher
## リフターのState
- Topic：(prefix)/collab/lifter/state
- Type：std_msgs/msg/String
- Usage：
```bash
```

## リフターのResult
- Topic：(prefix)/collab/lifter/result
- Type：std_msgs/msg/String
- Usage：
```bash
```

# （下位との通信）Subscriber
## リフター準備のState
- Topic：(prefix)/lifter/state/$(HASH)
- Type：std_msgs/msg/String
- Usage：
```bash
```

## リフター動作のResult
- Topic：(prefix)/lifter/result/$(HASH)
- Type：std_msgs/msg/String
- Usage：
```bash
```

# （下位との通信）Publisher
## リフター動作のRequest
- Topic：(prefix)/drive/run_lifter/$(HASH)
- Type：std_msgs/msg/String
- Usage：
```bash
# 上げるとき
ros2 topic pub -1 /drive/run_lifter/$(HASH) std_msgs/msg/String {data: "100"}
# 下げるとき
ros2 topic pub -1 /drive/run_lifter/$(HASH) std_msgs/msg/String {data: "-100"}
```
