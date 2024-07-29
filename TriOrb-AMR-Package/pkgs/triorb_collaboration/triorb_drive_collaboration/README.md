# Package: triorb_drive_collaboration


## [triorb_drive_collaboration Types](../TriOrb-ROS2-Types/triorb_drive_collaboration/README.md)

## Debug msg publish
```bash
docker attach global
ros2 topic pub -r 10 -t 60 /broadcast/joy sensor_msgs/Joy "{header:{stamp:{sec: 0, nanosec: 0}, frame_id: 'sample_payload'}, axes:[0.0,0.8,0.0]}"
ros2 topic pub -r 10 -t 10 /broadcast/joy sensor_msgs/Joy "{header:{stamp:{sec: 0, nanosec: 0}, frame_id: 'sample_payload'}, axes:[0.0,0.0,0.0]}"
ros2 topic pub -r 10 -t 20 /broadcast/joy sensor_msgs/Joy "{header:{stamp:{sec: 0, nanosec: 0}, frame_id: 'sample_payload'}, axes:[0.5,0.0,0.0]}"
ros2 topic pub -r 10 -t 10 /broadcast/joy sensor_msgs/Joy "{header:{stamp:{sec: 0, nanosec: 0}, frame_id: 'sample_payload'}, axes:[0.0,0.0,0.0]}"
```