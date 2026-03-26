# triorb_streaming_images

**パス**: `triorb_sensor/triorb_streaming_images`  
**説明**: 映像配信のためのパッケージ

## Package: triorb_streaming_images
このパッケージは、ROS 2 の `sensor_msgs/msg/Image` トピックから画像をサブスクリプションし、圧縮後に **MQTT トピックへ配信**するストリーミングノードです。

---

###  v1.2.0 変更点

- **画像配信方式が MQTT に移行**しました（従来のWebSocket配信は廃止）
- ROS 2 トピックから受信した画像を `.webp` 形式で圧縮
- Base64 エンコードし、MQTT ブローカーへ配信します

---

### Subscriber
####  `sensor_msgs/msg/Image`
- Topic: (可変)
- Type: sensor_msgs/msg/Image

### Publisher
####  MQTT 出力
- **Payload**: `.webp` 形式に圧縮 → Base64 文字列にエンコード
- **Topic**: `camera/stream`
- **Protocol**: `paho-mqtt` による MQTT publish

