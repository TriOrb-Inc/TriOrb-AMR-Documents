# sick_flexi_soft

**パス**: `triorb_sensor/sick/sick_Flexi-Soft_ROS2/src`  
**説明**: SICK PLCとEIP通信するためのパッケージ

## sick_flexi_soft

Flexi Soft PLC の Input/Output アセンブリデータを ROS に橋渡しします。

### Active API

#### Flexi Soft入力バッファ配信
- Topic：flexisoft/<assembly>/in_raw
- Node：(prefix)_sick_flexi_soft
- Type： std_msgs/msg/UInt8MultiArray
- Note：SensorDataQoS。EDS で検出した全 Input アセンブリ分の Raw バイト列を publish
- Usage：
```
ros2 topic echo flexisoft/standard_input/in_raw
```

#### Flexi Soft出力バッファ受付
- Topic：flexisoft/<assembly>/out_raw
- Node：(prefix)_sick_flexi_soft
- Type： std_msgs/msg/UInt8MultiArray
- Note：ParametersQoS。O->T データを書き戻すと PLC の出力マップに反映されます
- Usage：
```
ros2 topic pub flexisoft/standard_output/out_raw std_msgs/msg/UInt8MultiArray "{data: [1,0,0,0]}" --once
```

