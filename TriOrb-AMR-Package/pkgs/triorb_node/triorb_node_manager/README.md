# Package: triorb_node_manager

### Node一覧取得
- Topic：(prefix)/get/node/state
- Node：(prefix)_node_manager
- Type：triorb_static_interface/srv/NodeInfo
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/node/state triorb_static_interface/srv/NodeInfo
...
response:
triorb_static_interface.srv.NodeInfo_Response(result=[triorb_static_interface.msg.NodeInfo(name='/node_manager', state='awake'), triorb_static_interface.msg.NodeInfo(name='/os_setting', state='awake')])
```

### Node起動/終了
- Topic：(prefix)/node/state
- Node：(prefix)_node_manager
- Type：triorb_static_interface/msg/NodeInfo
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 topic pub -1 /node/state triorb_static_interface/msg/NodeInfo '{name: }'
...
response:
triorb_static_interface.srv.NodeInfo_Response(result=[triorb_static_interface.msg.NodeInfo(name='/node_manager', state='awake'), triorb_static_interface.msg.NodeInfo(name='/os_setting', state='awake'), triorb_static_interface.msg.NodeInfo(name='', state='awake'), ..., triorb_static_interface.msg.NodeInfo(name='triorb_navigate_cpp', state='sleep')])
```


## [ROSノード制御Types](../TriOrb-ROS2-Types/triorb_static_interface/README.md)