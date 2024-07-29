[../](../README.md)

# Package: triorb_drive_interface
## triorb_drive_interface Types

### triorb_drive_interface/msg/MotorParams
```bash
bool lpf                # Use LPF for driving command filter (False: moving average)
uint8 filter_t          # Command filter time constant (0-200)[ms]
uint8 pos_p_gain        # Position loop gain (1-50)[Hz]
uint16 speed_p_gain     # speed loop gain (1-500) [Hz]
uint16 speed_i_gain     # speed loop integral time constant (1-10000) [0.01ms]
uint16 torque_filter    # torque filter (0-4700) [Hz]
uint8 speed_ff          # speed feed-forward (0-100) [%]
uint8 stiffness         # machine stiffness selection (0-15)
```

### triorb_drive_interface/srv/MotorParams
```bash
std_msgs/Empty request
---
MotorParams result
```

### triorb_drive_interface/msg/MotorStatus
```bash
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

### triorb_drive_interface/srv/MotorStatus
```bash
std_msgs/Empty request
---
MotorStatus result
```

### triorb_drive_interface/msg/DriveGains
```bash
float32 xy_p    # translation P gain
float32 xy_i    # translation I gain (0 recommended)
float32 xy_d    # translation D gain
float32 w_p     # rotation P gain
float32 w_i     # rotation I gain (0 recommended)
float32 w_d     # rotation D gain
```

### triorb_drive_interface/msg/TriorbPos3
```bash
float32 x       # [m]
float32 y       # [m]
float32 deg     # [deg]
```

### triorb_drive_interface/msg/TriorbRunPos3
```bash
TriorbSpeed speed
TriorbPos3 position
```

### triorb_drive_interface/msg/TriorbRunResult
```bash
bool success
TriorbPos3 position
```

### triorb_drive_interface/msg/TriorbRunSetting
```bash
float32 tx      # Target error in X-axis direction [±m]
float32 ty      # Target error in Y-axis direction [±m].
float32 tr      # Target error in rotation [±deg].
uint8 force     # Target force level
```

### triorb_drive_interface/msg/TriorbRunVel3
```bash
TriorbSpeed speed
TriorbVel3 velocity
```

### triorb_drive_interface/msg/TriorbSetPos3
```bash
TriorbRunPos3 pos
TriorbRunSetting setting
```

### triorb_drive_interface/msg/TriorbSetPath
```bash
TriorbSetPos3[] path
```

### triorb_drive_interface/msg/TriorbSpeed
```bash
uint32 acc  # Acceleration time [ms]
uint32 dec  # Deceleration time [ms]
float32 xy  # Translation velocity [m/s]
float32 w   # Rotation speed [rad/s]
```

### triorb_drive_interface/msg/TriorbVel3
```bash
float32 vx # Velocity vector along X axis [m/s]
float32 vy # Velocity vector along Y axis [m/s]
float32 vw # Rotation velocity vector around the Z axis [rad/s]
```

### triorb_drive_interface/srv/TriorbRunPos3
```bash
TriorbRunPos3 request
---
std_msgs/Header header
uint8 result
```

### triorb_drive_interface/srv/TriorbRunVel3
```bash
TriorbRunVel3 request
---
std_msgs/Header header
uint8 result
```

### triorb_drive_interface/srv/TriorbSetPos3
```bash
TriorbSetPos3 pos
---
TriorbRunResult result
```

### triorb_drive_interface/srv/GetPath
```bash
TriorbPos3[] waypoint
---
TriorbPos3[] result
```

### triorb_drive_interface/action/TriorbSetPath
```bash
TriorbSetPos3[] path     # List of waypoints and movement control values for each waypoint
---
uint32 way_idx           # Index of waypoint currently moving
TriorbPos3 now           # Current robot position
---
TriorbRunResult result   # Result of completion of movement to final destination
```

### triorb_drive_interface/msg/Route
```bash
uint32 id               # ID
string name             # Name
TriorbPos3[] waypoint   # Waypoints
```

### triorb_drive_interface/srv/GetRoute
```bash
std_msgs/Empty request
---
Route result
```

### triorb_drive_interface/msg/TriorbAlignPos3
```bash
uint16[] marker_id          # 位置合わせ原点とするマーカーのID
float32[] marker_size       # マーカーのサイズ
TriorbRunPos3[] pos         # 原点に対する相対位置決め位置姿勢
TriorbRunSetting setting    # 走行設定
```