# triorb_sls_wrapper

**パス**: `triorb_sensor/sick/triorb_sick_sls_wrapper`  
**説明**: 
    Convert SICK SLS RawMicroScanData topics into sensor_msgs/PointCloud messages.
  

## triorb_sls_wrapper

RawMicroScanData を OccupancyGrid / PointCloud へ変換するノード群です。

### Active API

#### RawMicroScanData購読
- Topic：(prefix)/sick/raw_data （`input_topic` で変更可）
- Node：(prefix)_raw_data_to_occupancy / (prefix)_raw_data_to_pointcloud
- Type： sick_safetyscanners2_interfaces/msg/RawMicroScanData
- Note：SensorDataQoS。シリアル番号や config に応じて自動フィルタリング
- Usage：
```
ros2 topic echo /sick/raw_data
```

#### OccupancyGrid出力
- Topic：(prefix)/sick/occupancy （`occupancy_topic` / 個別設定で変更可）
- Node：(prefix)_raw_data_to_occupancy
- Type： nav_msgs/msg/OccupancyGrid
- Note：シリアル番号ごとにトピックを自動生成し、キャリブレーションに沿って 2D 投影
- Usage：
```
ros2 topic echo /sick/occupancy
```

#### PointCloud出力
- Topic：(prefix)/sick/pointcloud （`pointcloud_topic` で変更可）
- Node：(prefix)_raw_data_to_pointcloud
- Type： sensor_msgs/msg/PointCloud
- Note：Z 成分に反射強度を格納。必要に応じて `enable_pointcloud_debug_plot` を有効化
- Usage：
```
ros2 topic echo /sick/pointcloud
```

