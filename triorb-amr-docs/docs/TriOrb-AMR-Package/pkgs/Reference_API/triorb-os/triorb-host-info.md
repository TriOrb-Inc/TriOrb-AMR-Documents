# triorb_host_info

**パス**: `triorb_os/triorb_host_info`  
**説明**: ホストコンピューター（Jetson）関連の情報を表示するためのパッケージ

## triorb_host_info

ホストコンピューター（Jetson）関連の情報を表示するためのパッケージ

### ホストコンピュータのシステムモニター
Topic：(prefix)/host/status
Type：triorb_static_interface/msg/HostStatus
Frequency：1/1.0 Hz
Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic echo --once /host/status
header:
  stamp:
    sec: 1753410530
    nanosec: 830279666
  frame_id: host_device
memory_percent: 39.599998474121094
cpu_percent: 86.9000015258789
host_temperature: 70.81199645996094
wlan_ssid: TriOrb-WiFi
wlan_signal: 58
wlan_freq: 5180
ping: 10.668999671936035
gateway:
- 192
- 168
- 25
- 1
---
```

