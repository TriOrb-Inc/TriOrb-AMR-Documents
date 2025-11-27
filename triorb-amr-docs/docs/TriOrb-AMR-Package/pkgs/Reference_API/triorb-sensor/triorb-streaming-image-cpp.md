# triorb_streaming_image_cpp

**パス**: `triorb_sensor/triorb_streaming_image_cpp`  
**説明**: TODO: Package description

## Package: triorb_streaming_image_cpp
このパッケージは、ROS 2 の `sensor_msgs/msg/Image` トピックから画像をサブスクリプションし、圧縮後に **MQTT トピックへ配信**するストリーミングノードです。 <br>
python版(triorb_streaming_images)の代替パッケージであり、処理負荷軽減のためv1.2.3から追加されました。

---

###  更新履歴

---

### Subscriber
####  `sensor_msgs/msg/Image`
- Topic: (可変)
- Type: sensor_msgs/msg/Image

### Publisher
####  MQTT 出力
- **Payload**: `.webp`, `.jpg`, `.png` 形式に圧縮 → Base64 文字列にエンコード
- **Topic**: `camera/stream`
- **Protocol**: `paho-mqtt` による MQTT publish

### Parameter
| param | note | type | default |
|----------|----------|----------|----------|
| mqtt_address | MQTT Broker Address | string | localhost |
| mqtt_port | MQTT Broker Port | int | 1883 |
| mqtt_client_id | MQTT Client ID | string | triorb_streamer_{PID} |
| mqtt_topic | MQTT Topic | string | camera/stream |
| topic_name_raw | ROS2 topic name | string | /camera0 |
| scale | Stream scale | double | 0.2 |
| fps | Stream fps | double | 1.0 |
| quality | Image quality | int | 20 |
| encode | Encode format | string | webp |

#### note
- CPU usage: jpg < webp << png
- network trafic: webp < jpg <<< png
