# triorb_streaming_image_cpp

**パス**: `triorb_sensor/triorb_streaming_image_cpp`  
**説明**: カメラのImageトピックを購読し、JPEG/WEBP等へ圧縮してMQTTへ送出する軽量ストリーミングノードのC++実装です。

## triorb_streaming_image_cpp

カメラのImageトピックを購読し、JPEG/WEBP等へ圧縮してMQTTへ送出する軽量ストリーミングノードのC++実装です。

### Subscriber
####  `sensor_msgs/msg/Image`
- Topic: (可変)
- Type: sensor_msgs/msg/Image

### Publisher
####  MQTT 出力
- **Payload**: `.webp`, `.jpg`, `.png` 形式に圧縮 → Base64 文字列にエンコード
- **Topic**: `camera/stream`
- **Protocol**: `paho-mqtt` による MQTT publish
