# Package: triorb_vslam_tf


## 更新履歴
### 1.1.0
- tf_broadcast時の robot および rig にprefixを追加
  - ROS_LOCALHOST_ONLY=0のロボットが複数いる場合に別ロボットの姿勢を参照することがある問題の対策のため

## Subscriber
### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

## Publisher
### ロボット現在位置 
- Topic: (prefix)/vslam/rig_tf
- Type: geometry_msgs/msg/TransformStamped
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 topic echo --once /vslam/rig_tf 
header: 
  stamp: 
    sec: 1715249621 
    nanosec: 829307689 
  frame_id: triorb_map 
child_frame_id: robot 
transform: 
  translation: 
    x: 0.20051919812047725 
    y: -0.10789784916572422 
    z: -0.11166990297891966 
  rotation: 
    x: -0.0017948546889115379 
    y: -0.006014784536615234 
    z: 0.005654869190860537 
    w: 0.9999643110221774
```

### ロボット現在位置（平面内）
- Topic: (prefix)/vslam/robot_pose
- Type: triorb_drive_interface/msg/TriorbPos3
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 topic echo --once /vslam/robot_pose
x: 0.06437481194734573
y: 0.05932913348078728
deg: 4.468038082122803
```

## Service
### Description
- Topic: 
- Type: 
- Usage: 
```bash
```

## Action
### Description
- Topic: 
- Type: 
- Usage: 
```bash
```