# triorb_sick_plc_wrapper

**パス**: `triorb_sensor/sick/triorb_sick_plc_wrapper`  
**説明**: SICK製PLCとのEtherNet/IPデータ交換を行い、速度ベクトルや安全入出力をROS 2メッセージとPLCアセンブリ間で変換するラッパーノードです。

## triorb_sick_plc_wrapper

SICK製PLCとのEtherNet/IPデータ交換を行い、速度ベクトルや安全入出力をROS 2メッセージとPLCアセンブリ間で変換するラッパーノードです。


### Node interface
| Direction | Topic | Type | Notes |
|-----------|-------|------|-------|
| Subscribe | `/<prefix>/drive/std_vector2` | `std_msgs/msg/Float32MultiArray` | `[direction(rad), speed(m/s), rotate(rad/s)]`. Direction, speed, and rotate are scaled and packed into the outbound PLC assembly. |
| Subscribe | `/<prefix>/collab/alive` | `std_msgs/msg/Header` | Collaboration alive heartbeat. Sets `is_collab` bit in application data. |
| Subscribe | `/<prefix>/flexisoft/Assem131/in_raw` (configurable) | `std_msgs/msg/UInt8MultiArray` | PLC inbound assembly. `topic_from_plc` selects the topic; `sub_basic_index` chooses the byte that holds basic status bits. |
| Publish   | `/<prefix>/flexisoft/Assem141/out_raw` (configurable) | `std_msgs/msg/UInt8MultiArray` | PLC outbound assembly populated with scaled velocity vectors and control bits. `topic_to_plc` selects the topic. |
| Publish   | `/<prefix>/except_handl/node/add` | `std_msgs/msg/String` | Registers the node with the global exception handler when coming online. |
| Publish   | `/<prefix>/triorb/error/str/add` | `std_msgs/msg/String` | Emits error diagnostics (e.g., PLC buffer overruns or scaling limits). |
| Publish   | `/<prefix>/triorb/warn/str/add` | `std_msgs/msg/String` | Emits warnings (e.g., short PLC assemblies). |
| Service   | `/<prefix>/srv/plc/emergency_stop/request` | `std_srvs/srv/Trigger` | Raises the PLC emergency-stop bit once and acknowledges the request. |
| Service   | `/<prefix>/srv/plc/change_to_plc_off` | `std_srvs/srv/SetBool` | `true` → request PLC deactivate, `false` → cancel the request. |
| Service   | `/<prefix>/srv/sls/change_to_sls_off` | `std_srvs/srv/SetBool` | `true` → request SLS monitor OFF, `false` → SLS ON. |

