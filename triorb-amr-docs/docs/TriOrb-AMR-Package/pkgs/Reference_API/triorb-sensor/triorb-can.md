# triorb_can

**パス**: `triorb_sensor/triorb_can`  
**説明**: SocketCANを用いてCANバスとROS 2トピック（/can_bridge/rx, /can_bridge/tx）を相互接続するブリッジパッケージです。

## triorb_can
SocketCANを用いてCANバスとROS 2トピック（/can_bridge/rx, /can_bridge/tx）を相互接続するブリッジパッケージです。

## CAN Bridge Node  
**ROS 2 API 仕様書**

---

### 1. 概要
`CanBridgeNode` は、Linux SocketCAN (`PF_CAN`) を用いて  
**CAN バスと ROS 2 トピックを相互接続するブリッジノード**です。

- CAN → ROS 2（RX）
- ROS 2 → CAN（TX）

を非同期で処理します。

---

### 2. 責務範囲

#### 本ノードの責務
- SocketCAN を用いた CAN フレームの送受信
- CAN フレームを ROS 2 メッセージへ変換
- ROS 2 メッセージを CAN フレームへ変換
- YAML 設定による CAN ID フィルタリング
- 非同期 I/O による低レイテンシ通信

#### 本ノードの非責務
- CAN データの意味解釈（バッテリー/センサ等）
- 上位ロジック（制御・判断）
- CAN デバイス設定（bitrate 等）

---

### 3. ノード情報

| 項目 | 内容 |
|---|---|
| パッケージ名 | triorb_can_bridge |
| 実行ファイル | can_bridge |
| ノード名 | can_bridge（NODE_NAME マクロ依存） |
| 通信方式 | SocketCAN (RAW) |
| QoS | BestEffortOneQoS (KeepLast=1, Reliability=BestEffort, Durability=Volatile) |

---

### 4. ROS インタフェース

#### 4.1 Subscribe トピック（TX）

##### `/can_bridge/tx`
型：`triorb_sensor_interface::msg::CanFrame`

ROS から CAN へ送信されるフレーム。

---

#### 4.2 Publish トピック（RX）

##### `/can_bridge/rx`
型：`triorb_sensor_interface::msg::CanFrame`

CAN から受信したフレーム。

---

### 5. ROS メッセージ仕様

#### CanFrame
| フィールド | 型 | 説明 |
|---|---|---|
| `id` | uint32 | CAN ID |
| `dlc` | uint8 | データ長 |
| `data[8]` | uint8[] | Payload |
| `is_extended` | bool | 拡張 ID フラグ |
| `is_rtr` | bool | RTR フラグ |
| `is_error` | bool | Error フラグ |

---

### 6. 設定ファイル（YAML）

#### 6.1 設定ファイル指定
ROS パラメータで YAML ファイルのパスを指定します。

```bash
ros2 run triorb_can_bridge can_bridge \
  --ros-args -p config_path:=/ws/params/can.yaml
```

---

#### 6.2 YAML 構成例（can.yaml）
```yaml
CAN_INTERFACE: can0

RX_TOPIC: can_bridge/rx
TX_TOPIC: can_bridge/tx

## 受信許可 ID（空の場合は全受信）
RX_FRAME_IDS:
  - "0x053"
  - "0x056"
  - "0x076"

## 送信許可 ID（ホワイトリスト）
TX_ALLOW_IDS:
  - "0x100"
  - "0x200"

## TX のデフォルト拡張 ID 設定
TX_IS_EXTENDED_DEFAULT: false
```

---

### 7. CAN RX 動作仕様

- `RX_FRAME_IDS` が未指定または空：
  - **全 CAN フレームを受信**
- 指定あり：
  - SocketCAN の HW フィルタで受信制限
- 標準 ID / 拡張 ID 両対応
- 受信フレームは即座に `/can_bridge/rx` に publish

---

### 8. CAN TX 動作仕様

- `/can_bridge/tx` を subscribe
- `TX_ALLOW_IDS` が設定されている場合：
  - ホワイトリスト外 ID は送信拒否
- 拡張 ID 判定ルール：
  - msg.is_extended が true
  - または ID > 0x7FF
  - または `TX_IS_EXTENDED_DEFAULT == true`

---

### 9. 内部処理フロー

#### RX（CAN → ROS）
1. SocketCAN で CAN フレーム受信
2. フラグ・ID・Payload を CanFrame に変換
3. `/can_bridge/rx` に publish
4. 非同期で次の受信待ち

#### TX（ROS → CAN）
1. `/can_bridge/tx` を subscribe
2. ID ホワイトリスト判定
3. 拡張/標準 ID 判定
4. SocketCAN へ非同期送信

---

### 10. エラーハンドリング

| ケース | 挙動 |
|---|---|
| socket 作成失敗 | 例外送出 + error publish |
| bind 失敗 | ノード停止 |
| TX ID 不許可 | warn ログ + 送信抑止 |
| 非同期 I/O エラー | error ログ |

---

### 11. 実行方法

#### ビルド
```bash
colcon build --packages-select triorb_can_bridge
source install/setup.bash
```

#### 実行
```bash
ros2 run triorb_can_bridge can_bridge \
  --ros-args -p config_path:=/ws/params/can.yaml
```

---

### 12. 注意事項（社内）

- CAN bitrate 設定は OS 側で事前設定すること
- RX フィルタは HW レベルで適用される
- 受信順序保証なし（CAN 仕様準拠）
- リアルタイム用途では CPU affinity を検討

---

### 13. 更新履歴

| 日付 | 内容 |
|---|---|
| 2025-12-15 | 初版作成 |

---


