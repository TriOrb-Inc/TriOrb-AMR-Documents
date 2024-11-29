# Package: triorb_task_library
- タスク名とタスク内容の紐付け管理を行うパッケージ

## Service server
### Task descriptionの要求
- Service: (prefix)/fleet/srv/get_task_description
- Type: [triorb_static_interface/srv/SetString](../../TriOrb-ROS2-Types/triorb_static_interface/README.md#triorb_static_interfacesrvsetstring)
- Usage: 
```bash
root@aws-dev-arm-ubuntu22:/ws# ros2 service call /fleet/srv/get_task_description triorb_static_interface/srv/SetString 'request: ["sample_task_01"]'
requester: making request: triorb_static_interface.srv.SetString_Request(request=['sample_task_01'])

response:
triorb_static_interface.srv.SetString_Response(result='{"task_info":[{"mode":"pararell_move","move":[{"robot":"hostname1","route":[]},{"robot":"hostname2","route":[]}]},{"mode":"pararell_into","move":[{"robot":"hostname1","route":[]},{"robot":"hostname2","route":[]}]},{"direction":"up","mode":"sync_lift","move":[{"robot":"hostname1"},{"robot":"hostname2"}]},{"mode":"sync_move","robots":["hostname1","hostname2"],"waypoint_list":[[1.414,1.414,45.0,0.1,0.1,5.0],[2.0,2.0,90.0,0.01,0.01,1.0,0.1,0.3]]},{"direction":"down","mode":"sync_lift","move":[{"robot":"hostname1"},{"robot":"hostname2"}]},{"mode":"pararell_outof","move":[{"robot":"hostname1","route":[]},{"robot":"hostname2","route":[]}]}],"task_name":"sample_task_01","workers":["hostname1","hostname2"]}')
```

# Unit test
## 異常系
### 空リクエスト
```bash
root@aws-dev-arm-ubuntu22:/ws# ros2 service call /fleet/srv/get_task_description triorb_static_interface/srv/SetString 'request: []'
requester: making request: triorb_static_interface.srv.SetString_Request(request=[])

response:
triorb_static_interface.srv.SetString_Response(result='{"error":"request is empty"}')
```

### 存在しないタスク名
```bash
root@aws-dev-arm-ubuntu22:/ws# ros2 service call /fleet/srv/get_task_description triorb_static_interface/srv/SetString 'request: ["invalid_task_name"]'
requester: making request: triorb_static_interface.srv.SetString_Request(request=['invalid_task_name'])

response:
triorb_static_interface.srv.SetString_Response(result='{"error":"file not found: /triorb/params/fleet/task/invalid_task_name.json"}')
```

### json記法に誤りのあるタスク
```bash
root@aws-dev-arm-ubuntu22:/ws# ros2 service call /fleet/srv/get_task_description triorb_static_interface/srv/SetString 'request: ["invalid_json_name"]'
requester: making request: triorb_static_interface.srv.SetString_Request(request=['invalid_json_name'])

response:
triorb_static_interface.srv.SetString_Response(result='{"error":"[json.exception.parse_error.101] parse error at line 2, column 5: syntax error while parsing object key - invalid literal; last read: \'{<U+000A>    i\'; expected string literal"}')
```
