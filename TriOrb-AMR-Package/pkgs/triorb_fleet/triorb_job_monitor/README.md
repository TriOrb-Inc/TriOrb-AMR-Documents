# Package: triorb_job_monitor


## [triorb_job_monitor Types](../TriOrb-ROS2-Types/triorb_job_monitor/README.md)


### jobに参加しているロボットの一覧要求
- Note: request[0]にjob名を設定するとカンマで区切られたhostnameのstringを返す.
- Service: (prefix)/fleet/srv/job_workers
- Type: [triorb_static_interface/srv/SetString](../../TriOrb-ROS2-Types/triorb_static_interface/README.md#triorb_static_interfacesrvsetstring)
- Usage: 
```bash
root@aws-dev-arm-ubuntu22:/ws# ros2 service call /fleet/srv/job_workers triorb_static_interface/srv/SetString "{ request: [sync_group] }"
requester: making request: triorb_static_interface.srv.SetString_Request(request=['sync_group'])

response:
triorb_static_interface.srv.SetString_Response(result='raspberrypi,orin-nx-721X')
```