# Package: triorb_navigation_navi
上位システム管理下における単体自律移動管理のためのパッケージ

# Parameter
- ROBOT_TIMEOUT_MS : ロボットの自己位置が返ってこない場合のタイムアウト処理時間[ms]

# Subscriber
## 単体自律移動開始Request
- Topic: (prefix)/collab/move/request
- Type： std_msgs/msg/String
- Usate：
```bash
# triorb_drive_interface/msg/TriorbSetPos3型相当を含んだメッセージを送信する
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/move/request std_msgs/msg/String \
"{data : '{\
    "'"name"'" : "'"test_job_001"'",\
    "'"robot"'" : "'"TestMutex1"'",\
    "'"route"'" : [\
        {\
            "'"pos"'" : \
                {\
                "'"speed"'" : \
                    {\
                        "'"acc"'" : 1000,\
                        "'"dec"'" : 1000,\
                        "'"xy"'" : 0.5,\
                        "'"w"'" : 1.5\
                    },\
                "'"position"'" : \
                    {\
                        "'"x"'" : 0.0,\
                        "'"y"'" : 0.0,\
                        "'"deg"'" : 0.0\
                    }\
            },\
            "'"setting"'" : \
                {\
                    "'"tx"'" : 0.01,\
                    "'"ty"'" : 0.01,\
                    "'"tr"'" : 0.5,\
                    "'"force"'" : 1\
            }\
        },\
        {\
            "'"pos"'" : \
                {\
                "'"speed"'" : \
                    {\
                        "'"acc"'" : 1000,\
                        "'"dec"'" : 1000,\
                        "'"xy"'" : 0.5,\
                        "'"w"'" : 1.5\
                    },\
                "'"position"'" : \
                    {\
                        "'"x"'" : 0.5,\
                        "'"y"'" : 0.2,\
                        "'"deg"'" : 15.0\
                    }\
            },\
            "'"setting"'" : \
                {\
                    "'"tx"'" : 0.01,\
                    "'"ty"'" : 0.01,\
                    "'"tr"'" : 0.5,\
                    "'"force"'" : 1\
            }\
        }\
    ]\
}'}"
```

## 単体自律移動中断Request
- Topic: (prefix)/collab/move/terminate
- Type： std_msgs/msg/String

# Publisher
## 単体自律移動Status
- Topic: (prefix)/collab/move/state
- Type： std_msgs/msg/String
- 
## 単体自律移動Result
- Topic: (prefix)/collab/move/result
- Type： std_msgs/msg/String

# Publisher to robot
## 位置決め開始指示
- Topic: (prefix)/drive/set_pos/$(HASH)
- Type： triorb_drive_interface/msg/TriorbSetPos3

## 位置決め中止指示
- Topic: (prefix)/drive/stop/$(HASH)
- Type： std_msgs/msg/Empty

# Subscriber from robot
## 現在位置姿勢
- Topic: (prefix)/vslam/rig_tf/$(HASH)
- Type： geometry_msgs/msg/TransformStamped

## 位置決め実行結果
- Topic: (prefix)/drive/result/$(HASH)
- Type： triorb_drive_interface/msg/TriorbRunResult

# Unit Test
```bash
tobeta@orin-nx-4944:/home/triorb/TriOrb-AMR-Package-Collab$ sh run_mutex_manager.sh
tobeta@orin-nx-4944:/home/triorb/TriOrb-AMR-Package-Collab$ sh run_mapping.sh
（VSLAMで適当にマッピング）
tobeta@orin-nx-4944:/home/triorb/TriOrb-AMR-Package-Collab$ sh dev_navinavi.sh
tobeta@orin-nx-4944:/home/triorb/TriOrb-AMR-Package-Collab$ docker attach dev_navinavi_global
root@orin-nx-4944:/ws# source install/setup.bash
root@orin-nx-4944:/ws# ros2 topic pub -1 /collab/mutex/lock_mutex std_msgs/msg/String "{data : '{\
    "'"hash"'" : "'"TOBETA5"'",\
    "'"host"'" : "'"orin-nx-4944"'"\
}'}"
root@orin-nx-4260:/ws# ros2 topic pub -1 /collab/move/request std_msgs/msg/String \
"{data : '{\
    "'"name"'" : "'"test_job_001"'",\
    "'"robot"'" : "'"TOBETA5"'",\
    "'"route"'" : [\
        {\
            "'"pos"'" : \
                {\
                "'"speed"'" : \
                    {\
                        "'"acc"'" : 1000,\
                        "'"dec"'" : 1000,\
                        "'"xy"'" : 0.5,\
                        "'"w"'" : 1.5\
                    },\
                "'"position"'" : \
                    {\
                        "'"x"'" : 0.0,\
                        "'"y"'" : 0.0,\
                        "'"deg"'" : 0.0\
                    }\
            },\
            "'"setting"'" : \
                {\
                    "'"tx"'" : 0.01,\
                    "'"ty"'" : 0.01,\
                    "'"tr"'" : 0.5,\
                    "'"force"'" : 1\
            }\
        },\
        {\
            "'"pos"'" : \
                {\
                "'"speed"'" : \
                    {\
                        "'"acc"'" : 1000,\
                        "'"dec"'" : 1000,\
                        "'"xy"'" : 0.5,\
                        "'"w"'" : 1.5\
                    },\
                "'"position"'" : \
                    {\
                        "'"x"'" : 0.0,\
                        "'"y"'" : -0.1,\
                        "'"deg"'" : 0.0\
                    }\
            },\
            "'"setting"'" : \
                {\
                    "'"tx"'" : 0.01,\
                    "'"ty"'" : 0.01,\
                    "'"tr"'" : 0.5,\
                    "'"force"'" : 1\
            }\
        }\
    ]\
}'}"
root@orin-nx-4944:/ws# ros2 topic echo -f /collab/move/result
data: '{"name":"test_job_001","robot":{"\"TOBETA5\"":{"position":{"deg":-0.0004819970480767799,"x":0.00335985430369203,"y":-0.0926972255213332},"status":"success","success":true}},"status":"success"}'
---
```