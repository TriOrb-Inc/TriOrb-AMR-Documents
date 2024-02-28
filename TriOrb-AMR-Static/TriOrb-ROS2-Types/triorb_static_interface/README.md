[../](../README.md)

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

### triorb_static_interface/msg/NodeInfo
```bash
string name # Node name
string state # Node state ( sleep | wakeup | awake )
```

### triorb_static_interface/srv/NodeInfo
```bash
std_msgs/Empty request
---
NodeInfo[] result
```

### triorb_static_interface/msg/HostStatus
```bash
std_msgs/Header header      # Timestamp
float32 memory_percent      # Memory usage
float32 cpu_percent         # CPU usage
float32 host_temperature    # Temperature of the host computer
string wlan_ssid            # SSID of the access point
uint8 wlan_signal           # Signal strength of the access point 
uint32 wlan_freq            # Communication speed of the access point
float32 ping                # Ping speed to the default gateway
uint8[] gateway             # Address of the default gateway
```