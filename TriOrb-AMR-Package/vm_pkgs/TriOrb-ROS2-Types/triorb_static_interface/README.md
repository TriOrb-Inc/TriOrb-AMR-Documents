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

### triorb_static_interface/srv/Ros2Run
```bash
string pkg          # Package name
string exec         # Executable file name
string args         # Arguments to the executable
---
string result       # Execution result
```

### triorb_static_interface/srv/Ros2Launch
```bash
string pkg          # Package name
string file         # Launch file name
string args         # Arguments to the launch file
---
string result       # Launch result
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

### triorb_static_interface/msg/RobotStatus
```bash
std_msgs/Header header  # timestamp
float32 voltage         # main power supply voltage
uint16 btns             # Remote control operation status (bit flag)
uint16 state            # Robot operation state (bit flag)
uint16 error            # Error status of the robot (bit flag)

#---Remote control operation status (bit flag)---
# 0x8000: Remote control Y button
# 0x4000: Remote control B button
# 0x2000: Remote control A button
# 0x1000: Remote control X button

#---Robot operation state (bit flag)---
# 0x8000: Motor is being excited
# 0x4000: Accepting move instruction
# 0x2000: Moving
# 0x1000: Self-position recognition in progress
# 0x0800: Generating map
# 0x0400: During anti-collision control
# 0x0200: Position control move completed
# 0x0100: Interrupt move instruction disabled

#---Error status of the robot (bit flag)---
# 0x8000: Motor connection error
# 0x4000: IMU and distance sensor connection error
# 0x2000: Camera connection error
# 0x1000: Main power supply voltage abnormal
```

### triorb_static_interface/srv/GetString
```bash
std_msgs/Empty request
---
string result
```

### triorb_static_interface/srv/GetStringList
```bash
std_msgs/Empty request
---
string[] result
```

### triorb_static_interface/srv/SetString
```bash
string[] request
---
string result
```

### triorb_static_interface/srv/GetImage
```bash
std_msgs/Empty request
---
sensor_msgs/Image image
```

### triorb_static_interface/srv/SetImage
```bash
sensor_msgs/Image image
---
string result
```

