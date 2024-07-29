# TriOrb-ROS2-Types 1.0.0 (eb4962f)

# triorb_collaboration_interface 
## triorb_collaboration_interface/msg 
### triorb_collaboration_interface/msg/ParentBind.msg
```bash
# ==[協調搬送] 仮想（荷物など）原点に対するロボットの相対姿勢==
std_msgs/Header header      # Header
string parent               # Parent name
string you                  # Your name
float32 x                   # Relative position of the parent from you [m]
float32 y                   # Relative position of the parent from you [m]
float32 deg                 # Relative position of the parent from you [deg]
```

# triorb_cv_interface 
## triorb_cv_interface/msg 
### triorb_cv_interface/msg/BoundingBox.msg
```bash
# ==バウンディングボックス座標==
float32[] xtl_ytl_xbr_ybr       # [Left-top-x, Left-top-y, Right-bottom-x, Right-bottom-y] [pix]
```

### triorb_cv_interface/msg/Detection.msg
```bash
# ==物体検出結果==
std_msgs/Header header      # Timestamp
uint32 det_num              # Number of detections
BoundingBox[] boxes         # BoundingBoxs
float64[] scores            # Detection scores
string[] labels             # Object types
```

## triorb_cv_interface/srv 
# triorb_drive_interface 
## triorb_drive_interface/action 
### triorb_drive_interface/action/TriorbSetPath.action
```bash
#==[Action] Waypointリストを入力、途中経過を通知、完了ステータスを返却===
TriorbSetPos3[] path     # List of waypoints and movement control values for each waypoint
---
TriorbRunResult result   # Result of completion of movement to final destination
---
uint32 way_idx           # Index of waypoint currently moving
TriorbPos3 now           # Current robot position
```

## triorb_drive_interface/msg 
### triorb_drive_interface/msg/DriveGains.msg
```bash
#==自律移動のゲインパラメーター==
float32 xy_p    # translation P gain
float32 xy_i    # translation I gain (0 recommended)
float32 xy_d    # translation D gain
float32 w_p     # rotation P gain
float32 w_i     # rotation I gain (0 recommended)
float32 w_d     # rotation D gain
```

### triorb_drive_interface/msg/MotorParams.msg
```bash
#==モーター制御パラメーター==
bool lpf                # Use LPF for driving command filter (False: moving average)
uint8 filter_t          # Command filter time constant (0-200)[ms]
uint8 pos_p_gain        # Position loop gain (1-50)[Hz]
uint16 speed_p_gain     # speed loop gain (1-500) [Hz]
uint16 speed_i_gain     # speed loop integral time constant (1-10000) [0.01ms]
uint16 torque_filter    # torque filter (0-4700) [Hz]
uint8 speed_ff          # speed feed-forward (0-100) [%]
uint8 stiffness         # machine stiffness selection (0-15)
```

### triorb_drive_interface/msg/MotorStatus.msg
```bash
#==モーターステータス==
std_msgs/Header header      # Timestamp
uint16 last_error_value     # Last motor alert flag
uint8 last_error_motor      # Motor ID of the last alert
float32 voltage             # Mains voltage observed by the motor driver
uint16 state                # Operating state of each motor (bit flag)
float32 power               # Power consumption of each motor (W)

#---Operating state of each motor (bit flag)---
# 0x8000: Remote control Y button
# 0x4000: Remote control B button
# 0x2000: Remote control A button
# 0x1000: Remote control X button
# 0x0800: Rotating
# 0x0400: Position control complete
# 0x0200: Excitation in progress
# 0x0100: Motor status acquired successfully
```

### triorb_drive_interface/msg/Route.msg
```bash
#==自律移動経路==
uint32 id               # ID
string name             # Name
TriorbPos3[] waypoint   # Waypoints
```

### triorb_drive_interface/msg/TriorbPos3.msg
```bash
#==平面内の位置・姿勢==
float32 x       # [m]
float32 y       # [m]
float32 deg     # [deg]
```

### triorb_drive_interface/msg/TriorbRunPos3.msg
```bash
#==相対位置・姿勢指示による移動==
TriorbSpeed speed       # Configure of moving
TriorbPos3 position     # Target position
```

### triorb_drive_interface/msg/TriorbRunResult.msg
```bash
#==自律移動結果==
bool success                # Moving result (true: Compleat, false: Feild)
TriorbPos3 position         # Last robot position
```

### triorb_drive_interface/msg/TriorbRunSetting.msg
```bash
#==自律移動の位置決め設定==
float32 tx      # Target error in X-axis direction [±m]
float32 ty      # Target error in Y-axis direction [±m].
float32 tr      # Target error in rotation [±deg].
uint8 force     # Target force level
```

### triorb_drive_interface/msg/TriorbRunVel3.msg
```bash
#==速度指示による移動==
TriorbSpeed speed       # Configure of moving
TriorbVel3 velocity     # Target velocities
```

### triorb_drive_interface/msg/TriorbSetPos3.msg
```bash
#==目標位置・姿勢指示による移動==
TriorbRunPos3 pos           # Goal position
TriorbRunSetting setting    # Configure of navigation
```

### triorb_drive_interface/msg/TriorbSpeed.msg
```bash
#==加減速時間・速度の設定==
uint32 acc  # Acceleration time [ms]
uint32 dec  # Deceleration time [ms]
float32 xy  # Translation velocity [m/s]
float32 w   # Rotation speed [rad/s]
```

### triorb_drive_interface/msg/TriorbVel3.msg
```bash
#==平面内の移動速度設定==
float32 vx      # Velocity vector along X axis [m/s]
float32 vy      # Velocity vector along Y axis [m/s]
float32 vw      # Rotation velocity vector around the Z axis [rad/s]
```

## triorb_drive_interface/srv 
### triorb_drive_interface/srv/GetPath.srv
```bash
#==[Service] 経由点及び経路生成設定を入力、生成された経由点を取得==
TriorbPos3[] waypoint
uint8 dilation_k_size
uint8 gauss_k_size
float32 sigma
---
TriorbPos3[] result
```

### triorb_drive_interface/srv/GetRoute.srv
```bash
#==[Service] 現在の自律移動経路を取得==
std_msgs/Empty request
---
Route[] result
```

### triorb_drive_interface/srv/MotorParams.srv
```bash
#==[Service] モーターパラメーターを取得==
std_msgs/Empty request
---
MotorParams result
```

### triorb_drive_interface/srv/MotorStatus.srv
```bash
#==[Service] モーターステータスを取得==
std_msgs/Empty request
---
MotorStatus result
```

### triorb_drive_interface/srv/TriorbRunPos3.srv
```bash
#==[Service] 相対位置・姿勢指示による移動と結果の取得==
TriorbRunPos3 request
---
std_msgs/Header header
uint8 result
```

### triorb_drive_interface/srv/TriorbRunVel3.srv
```bash
#==[Service] 速度指示による移動と結果の取得==
TriorbRunVel3 request
---
std_msgs/Header header
uint8 result
```

### triorb_drive_interface/srv/TriorbSetPos3.srv
```bash
#==[Service] 目標位置・姿勢指示による移動と結果の取得==
TriorbSetPos3 pos
---
TriorbRunResult result
```

# triorb_field_interface 
## triorb_field_interface/msg 
### triorb_field_interface/msg/Keyframe.msg
```bash
#==Keyframe information==
uint32 id       # Frame id
float32 tvec    # Translation vector
float32 rvec    # Rotation vector
string name     # Name of the frame
```

## triorb_field_interface/srv 
### triorb_field_interface/srv/GetKeyframeList.srv
```bash
#==[Service] キーフレーム一覧を取得==
std_msgs/Empty request
---
Keyframe[] result
```

### triorb_field_interface/srv/InsertKeyframe.srv
```bash
#==[Service] 現在位置・姿勢のキーフレームを挿入する==
std_msgs/Empty request
---
string result               # Result of the inserting
Keyframe[] keyframe         # Inserted keyframes
```

# triorb_project_interface 
## triorb_project_interface/srv 
# triorb_sensor_interface 
## triorb_sensor_interface/action 
### triorb_sensor_interface/action/CameraCalibrationInternal.action
```bash
# ==[Action] カメラ内部パラメーターキャリブレーションの実行==
# 参考：https://developer.mamezou-tech.com/robotics/vision/calibration-pattern/#asymmetry-circlegrid
# 参考：https://calib.io/pages/camera-calibration-pattern-generator
# > Width 280mm, Height 200mm, Rows 11, Cols 16, Spacing 20mm, Diameter 12mm

# --- Goal ---
uint16 rows                             # Calibration board definition: Rows
uint16 cols                             # Calibration board definition: Columns
float32 spacing                         # Calibration board definition: Circle Spacing [mm]
float32 diameter                        # Calibration board definition: Diameter [mm]
string src                              # Calibration target (Topic / device path / directory path / movie file path)
---
# --- Result ---
sensor_msgs/CompressedImage image       # Calibration result
float32 fx
float32 fy
float32 cx
float32 cy
float32 k1
float32 k2
float32 k3
float32 k4
---
# --- Feedback ---
string progress
sensor_msgs/CompressedImage image       # Image on the way
```

## triorb_sensor_interface/msg 
### triorb_sensor_interface/msg/CameraDevice.msg
```bash
#==カメラデバイス==
string device       # Path of camera device
string topic        # Topic name of camera image
string id           # Frame ID of the camera image topic
string state        # Camera device status (sleep | wakeup | awake)
int16 rotation      # Rotation of the camera image
int16 exposure      # Camera Exposure
float32 gamma       # Gamma correction value
float32 timer       # Data collection cycle [s]
```

### triorb_sensor_interface/msg/DistanceSensor.msg
```bash
#==距離センサ==
std_msgs/Header header      # Timestamp
float32 distance      		# Distance to obstacle [m]
uint8 confidence            # Signal reliability (0-100)
float32 hfov                # Horizontal detectable angle [deg]
float32 vfov                # Vertical detectable angle [deg]
float32 max_dist            # Maximum detectable distance [m]
float32 min_dist            # Minimum detectable distance [m]
float32[] mount_xyz         # Mounting location [m]
float32[] mount_ypr         # Mounting orientation [deg]
```

### triorb_sensor_interface/msg/ImuSensor.msg
```bash
#==IMUセンサ==
std_msgs/Header header # Timestamp
float32 yaw
float32 pitch
float32 roll
```

### triorb_sensor_interface/msg/Obstacles.msg
```bash
#==障害物==
std_msgs/Header header      # Timestamp
float32 forward      		# Distance to obstacle in forward [m]
float32 left      		    # Distance to obstacle in left [m]
float32 right      		    # Distance to obstacle in right [m]
float32 back      		    # Distance to obstacle in back [m]
```

## triorb_sensor_interface/srv 
### triorb_sensor_interface/srv/CameraCapture.srv
```bash
#==[Service] カメラキャプチャ指示==
CameraDevice[] request
---
string[] result
```

### triorb_sensor_interface/srv/CameraDevice.srv
```bash
#==[Service] カメラキャプチャ一覧の取得==
std_msgs/Empty request
---
CameraDevice[] result
```

### triorb_sensor_interface/srv/GetDistanceSensor.srv
```bash
#==[Service] 距離センサ一覧の取得==
std_msgs/Empty request
---
string[] topic  # List of topic name
string[] state  # List of sensor state ( sleep | wakeup | awake )
```

### triorb_sensor_interface/srv/SetDistanceSensor.srv
```bash
#==[Service] 距離センサの設定指示==
string[] topic  # List of topic name
string[] state  # List of sensor state ( sleep | wakeup | awake )
---
string[] result
```

# triorb_static_interface 
## triorb_static_interface/msg 
### triorb_static_interface/msg/HostStatus.msg
```bash
#==ホストコンピューターのモニター==
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

### triorb_static_interface/msg/NodeInfo.msg
```bash
#==ROS2ノードの状態==
string name # Node name
string state # Node state ( sleep | wakeup | awake )
```

### triorb_static_interface/msg/RobotStatus.msg
```bash
#==ロボットの状態==
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

#---Error status of the robot (bit flag)---
# 0x8000: Motor connection error
# 0x4000: IMU and distance sensor connection error
# 0x2000: Camera connection error
# 0x1000: Main power supply voltage abnormal
```

### triorb_static_interface/msg/SettingIPv4.msg
```bash
#==TCP/IPv4==
string device # device name
string method # device mode: auto | manual | shared | disabled
uint8[] adress # IP adress
uint8 mask # Subnet mask
uint8[] gateway # Default gateway adress
uint8[] mac # Hardware adress
```

### triorb_static_interface/msg/SettingROS.msg
```bash
#==ROS2環境==
bool ros_localhost_only # ROS_LOCALHOST_ONLY
uint16 ros_domain_id # ROS_DOMAIN_ID
string ros_prefix # ROS_PREFIX
```

### triorb_static_interface/msg/SettingSSID.msg
```bash
#==無線LAN設定==
string ssid # Wi-Fi SSID name
string passphrase # Wi-Fi passphrase
string security # Wi-Fi security type
uint8 signal # Signal strength (0-100)
```

## triorb_static_interface/srv 
### triorb_static_interface/srv/GetImage.srv
```bash
#==[Service] 画像の取得==
std_msgs/Empty request
---
sensor_msgs/Image image
```

### triorb_static_interface/srv/GetString.srv
```bash
#==[Service] 文字列の取得==
std_msgs/Empty request
---
string result
```

### triorb_static_interface/srv/GetStringList.srv
```bash
#==[Service] 文字列リストの取得==
std_msgs/Empty request
---
string[] result
```

### triorb_static_interface/srv/NodeInfo.srv
```bash
#==[Service] ROS2ノード情報の取得==
std_msgs/Empty request
---
NodeInfo[] result
```

### triorb_static_interface/srv/SetImage.srv
```bash
#==[Service] 画像の入力==
sensor_msgs/Image image
---
string result
```

### triorb_static_interface/srv/SetString.srv
```bash
#==文字列の入力==
string[] request
---
string result
```

### triorb_static_interface/srv/SettingIPv4.srv
```bash
#==[Service] TCP/IPv4設定の取得==
std_msgs/Empty request
---
SettingIPv4[] result
```

### triorb_static_interface/srv/SettingROS.srv
```bash
#==[Service] ROS2環境設定の取得==
std_msgs/Empty request
---
SettingROS result
```

### triorb_static_interface/srv/SettingSSID.srv
```bash
#==[Service] 無線LAN設定の取得==
std_msgs/Empty request
---
SettingSSID[] result
```

