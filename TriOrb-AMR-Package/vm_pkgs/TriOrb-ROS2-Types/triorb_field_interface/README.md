[../](../README.md)

# Package: triorb_field_interface
## triorb_field_interface Types
### triorb_field_interface/msg/Keyframe
```bash
uint32 id       # Frame id
float32 tvec    # Translation vector
float32 rvec    # Rotation vector
string name     # Name of the frame
```

### triorb_field_interface/srv/GetKeyframeList
```bash
std_msgs/Empty request
---
Keyframe[] result
```

### triorb_field_interface/srv/SetKeyframe
```bash
Keyframe keyframe
---
string result
```