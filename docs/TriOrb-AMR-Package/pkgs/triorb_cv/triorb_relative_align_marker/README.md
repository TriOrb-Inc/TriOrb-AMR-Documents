# Package: triorb_relative_align_marker
## Requirements
```bash
python3 -m pip install pupil-apriltags
```

## カメラによるマーカー検出に基づくマーカー相対姿勢の推定
### Passive API
### マーカーに対するロボット相対姿勢
- Topic：(prefix)/relative_align_marker/transform
- Node：(prefix)_relative_align_marker
- Type：geometry_msgs/msg/TransformStamped
- Usage：
```bash
```

### Active API
### マーカーに対するロボット相対姿勢推定の開始
- Topic：(prefix)/relative_align_marker/start
- Node：(prefix)_relative_align_marker
- Type：std_msgs/msg/Bool
- Usage：
```bash
root@orin-nx-721X:/ws# ros2 topic pub -1 relative_align_marker/start std_msgs/msg/Bool
```

### マーカーに対するロボット相対姿勢推定の停止
- Topic：(prefix)/relative_align_marker/start
- Node：(prefix)_relative_align_marker
- Type：std_msgs/msg/Bool
- Usage：
```bash
```

## Overview
<img src="figs/overview.png" width="300">