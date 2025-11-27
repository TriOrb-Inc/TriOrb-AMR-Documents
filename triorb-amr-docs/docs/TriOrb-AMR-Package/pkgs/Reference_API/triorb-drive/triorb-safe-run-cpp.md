# triorb_safe_run_cpp

**パス**: `triorb_drive/triorb_safe_run_cpp`  
**説明**: C++ implementation of the TriOrb safe run velocity filter.

## triorb_safe_run_cpp

C++ implementation of TriOrb's safe run-velocity filter node. The node synchronizes SICK point cloud streams, builds a lightweight occupancy map, and publishes safer `/drive/run_vel` commands derived from `/safe_drive/run_vel` by means of a potential-field based repulsive force model.

### Node interface
| Direction | Topic | Type | Notes |
|-----------|-------|------|-------|
| Subscribe | `/<prefix>/sick/point2d/right` (configurable) | `sensor_msgs/msg/PointCloud` | Synchronized via ApproximateTime. `point2d_topics` can list two or more streams. |
| Subscribe | `/<prefix>/sick/point2d/left` (configurable) | `sensor_msgs/msg/PointCloud` | Same as above; add entries in config to change topics. |
| Subscribe | `/<prefix>/safe_drive/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3` | Raw velocity command to be filtered. |
| Publish   | `/<prefix>/drive/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3` | Safe velocity command after potential-field filtering. |
| Publish   | `/<prefix>/drive/set_life_time` | `std_msgs/msg/UInt16` | Optional watchdog lifetime (currently throttled). |
| Publish   | `/<prefix>/triorb_safe_run/debug/image/compressed` | `sensor_msgs/msg/CompressedImage` | Enabled when `enable_image_pub=true`; shows occupancy & vectors. |
| Publish   | `/<prefix>/except_handl/node/add` etc. | `std_msgs/msg/String` | Registration and diagnostic topics inherited from Python node. |
| Service   | `/<prefix>/triorb_safe_run/set_config` | `triorb_static_interface/srv/SetString` | Pass a JSON string (first element of `request[]`) to replace the runtime configuration. |
| Service   | `/<prefix>/triorb_safe_run/get_config` | `triorb_static_interface/srv/GetString` | Returns the current configuration as JSON text in `result`. |

Prefix depends on `ROS_PREFIX` env var (same mechanic as Python版) to allow namespace scoping.

### Repository layout
- `include/triorb_safe_run_cpp/` – public headers (`safe_run_node.hpp`).
- `src/` – node implementation (`safe_run_node.cpp`).
- `config/` – sample parameter files (copy `sample_config.json` and adjust per robot).
- `launch/` – placeholder for future launch files.

### Key features
- ApproximateTime synchronized `sensor_msgs::msg::PointCloud` subscribers.
- Occupancy map persistence with optional decay (`map_decay`).
- Angle-weighted potential forces with velocity bias (`velocity_bias`) to keep repulsion even when vehicle speeds are low.
- Safety controller that blends filtered velocity commands and republishes `/drive/run_vel`.
- Optional debug compressed image publisher (`enable_image_pub`).

### Building
```bash
colcon build --packages-select triorb_safe_run_cpp
source install/setup.bash
```

### Running
```bash
ros2 run triorb_safe_run_cpp safe_run_cpp_node --ros-args -p config_file:=/path/to/your_config.json
##ros2 run triorb_safe_run_cpp safe_run_cpp_node --ros-args -p config_file:=/ws/pkgs/triorb_drive/triorb_safe_run_cpp/config/sample_config.json
```
Common parameters (see `config/sample_config.json` for full list):
- `point2d_topics`: array of SICK point cloud topics.
- `point2d_topics_csv`: same as上記だがカンマ区切り文字列で指定したいときに使用 (`topic_a,topic_b,...`)。
- `anker_points`: footprint vertices used for potential anchor calculations (mm units).
- `anker_points_csv`: `x0,y0,x1,y1,...` 形式でアンカーポイントを一括指定。
- `force_coeff_linear`, `watch_angle_coeff`, `velocity_bias`: tune repulsive force behavior.
- `map_decay`: 0.0–1.0 blend factor to retain past obstacles.
- `ctrl_ms`, `vel_decay_coeff`, `vel_filter_weight`: control loop cadence and smoothing.

### Notes / Best practices
1. Ensure all `point2d_topics` publishers are available before launching; the node waits but exits if none are provided in the config.
2. Disable `map_decay` (set to 0) if you require instantaneous obstacle clearing; otherwise a small decay (e.g., 0.4) stabilizes noisy scans.
3. `watch_angle_coeff` compresses or widens the effective FOV of repulsion; smaller values help catch side obstacles.
4. When tuning, start with `velocity_bias = 0.0` and increase only if you need residual repulsion when nearly stopped.
5. For visualization, set `enable_image_pub=true` and inspect `/triorb_safe_run/debug/image/compressed`.

Contributions: please keep the README/Agent files updated as parameters or behavior change.

