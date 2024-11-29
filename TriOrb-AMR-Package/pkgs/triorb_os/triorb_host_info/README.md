# Package: triorb_host_info

## ホストコンピュータのシステムモニター
Topic：(prefix)/host/status
Type：triorb_static_interface/msg/HostStatus
Frequency：1/1.0 Hz
Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic echo --once /host/status
header:
  stamp:
    sec: 1709713301
    nanosec: 279324700
  frame_id: host_device
memory_percent: 11.899999618530273
cpu_percent: 1.899999976158142
host_temperature: 50.1870002746582
wlan_ssid: TriOrb-WiFi
wlan_signal: 75
wlan_freq: 5220
ping: 6.328000068664551
gateway:
- 192
- 168
- 21
- 1
---
```