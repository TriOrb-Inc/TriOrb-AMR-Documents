[../](../README.md)

# Package: triorb_sensor_interface
## triorb_sensor_interface Types
### triorb_sensor_interface/msg/DistanceSensor
```bash
std_msgs/Header header      # Timestamp
float32 distance      		# Distance to obstacle [m]
uint8 confidence            # Signal reliability (0-100)
```

### triorb_sensor_interface/msg/ImuSensor
```bash
std_msgs/Header header # Timestamp
float32 yaw
float32 pitch
float32 roll
```


### triorb_sensor_interface/msg/CameraDevice
```bash
string device       # Path of camera device
string topic        # Topic name of camera image
string id           # Frame ID of the camera image topic
string state        # Camera device status (sleep | wakeup | awake)
int16 rotation      # Rotation of the camera image
int16 exposure      # Camera Exposure
float32 gamma       # Gamma correction value
float32 timer       # Data collection cycle [s]
```

### triorb_sensor_interface/srv/CameraDevice
```bash
std_msgs/Empty request
---
CameraDevice[] result
```

### triorb_sensor_interface/srv/CameraCapture
```bash
CameraDevice[] request
---
string result
```

### triorb_sensor_interface/srv/GetDistanceSensor
```bash
std_msgs/Empty request
---
string[] topic  # List of topic name
string[] state  # List of sensor state ( sleep | wakeup | awake )
```

### triorb_sensor_interface/srv/SetDistanceSensor
```bash
string[] topic  # List of topic name
string[] state  # List of sensor state ( sleep | wakeup | awake )
---
string[] result
```

### triorb_sensor_interface/action/CameraCalibrationInternal
```bash
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

