[../](../README.md)

# Package: triorb_cv_interface
## triorb_cv_interface Types
### triorb_cv_interface/msg/BoundingBox
```bash
float32[] xtl_ytl_xbr_ybr
```

### triorb_cv_interface/msg/Detection
```bash
std_msgs/Header header      # Timestamp
uint32 det_num              # Number of detections
BoundingBox[] boxes         # BoundingBoxs
float64[] scores            # Detection scores
string[] labels             # Object types
```