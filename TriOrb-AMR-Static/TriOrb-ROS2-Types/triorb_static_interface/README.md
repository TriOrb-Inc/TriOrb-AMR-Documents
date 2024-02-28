# Package: triorb_static_interface
### triorb_static_interface/msg/SettingIPv4
```bash
string device # device name
string method # device mode: auto | manual | shared | disabled
uint8[] adress # IP adress
uint8 mask # Subnet mask
uint8[] gateway # Default gateway adress
uint8[] mac # Hardware adress
```
### triorb_static_interface/msg/SettingSSID
```bash
string ssid # Wi-Fi SSID name
string passphrase # Wi-Fi passphrase
string security # Wi-Fi security type
uint8 signal # Signal strength (0-100)
```
### triorb_static_interface/srv/SettingIPv4
```bash
std_msgs/Empty request
---
SettingIPv4[] result 
```
### triorb_static_interface/srv/SettingSSID
```bash
std_msgs/Empty request
---
SettingSSID[] result 
```

### triorb_static_interface/msg/SettingROS
```bash
bool ros_localhost_only # ROS_LOCALHOST_ONLY
uint16 ros_domain_id # ROS_DOMAIN_ID
string ros_prefix # ROS_PREFIX
```


### triorb_static_interface/srv/SettingROS
```bash
std_msgs/Empty request
---
SettingROS result
```

