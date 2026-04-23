# triorb_battery_info

**パス**: `triorb_os/triorb_battery_info`  
**説明**: CAN経由で受信したバッテリーSOC・各モジュール電圧/電流を集約し、/battery/status として配信するパッケージです。

## triorb_battery_info
CAN経由で受信したバッテリーSOC・各モジュール電圧/電流を集約し、/battery/status として配信するパッケージです。

## Battery Status Node  
**ROS 2 API 仕様書**

---

### 1. 概要
`BatteryStatusNode` は、CAN バスから受信したバッテリー情報を ROS 2 メッセージに変換し、  
システム全体で利用可能な **バッテリー状態トピック** を提供するノードです。

本ノードは以下を行います。

- CAN フレームから SOC（残容量）を取得
- 各バッテリーモジュールの電流・電圧を取得
- モジュール数に応じて情報を集約
- 直列 / 並列構成に応じたパック電圧を算出
- ROS 2 トピックとして定期 publish

---

### 2. 責務範囲

#### 本ノードの責務
- バッテリー SOC / モジュール IV の CAN デコード
- モジュール数 1 個以上への対応
- パック構成（直列 / 並列）の考慮
- パック全体電圧の算出
- BatteryStatus メッセージの publish

#### 本ノードの非責務
- バッテリー保護・遮断制御
- 異常判定・フェイルセーフ
- 充放電制御
- CAN 通信エラーの復旧処理

---

### 3. ノード情報

| 項目 | 内容 |
|---|---|
| パッケージ名 | triorb_battery_info |
| 実行ファイル | battery_status |
| ノード名 | battery_status（NODE_NAME マクロ依存） |
| Publish 周期 | 1 Hz |
| QoS | BestEffortOneQoS (KeepLast=1, Reliability=BestEffort, Durability=Volatile) |

---

### 4. ROS インタフェース

#### 4.1 Subscribe トピック

##### `/can_bridge/rx`
型：`triorb_sensor_interface::msg::CanFrame`

| フィールド | 説明 |
|---|---|
| `id` | CAN ID |
| `dlc` | データ長 |
| `data` | Payload (0–7 byte) |

---

#### 4.2 Publish トピック

##### `/battery/status`
型：`triorb_sensor_interface::msg::BatteryStatus`

###### BatteryStatus
| フィールド | 説明 |
|---|---|
| `remaining_mah` | バッテリー残容量（合算） |
| `remaining_percent` | SOC [%] |
| `total_voltage_v` | パック全体電圧 |
| `modules[]` | 各モジュール状態 |

###### BatteryModuleStatus
| フィールド | 説明 |
|---|---|
| `module_id` | モジュール番号（1始まり） |
| `voltage_v` | モジュール電圧 [V] |
| `current_a` | モジュール電流 [A] |

---

### 5. CAN フレーム仕様

#### 5.1 SOC フレーム

| 項目 | 内容 |
|---|---|
| CAN ID | `id_soc`（YAML指定） |
| DLC | 4 byte 以上 |

**Payload 定義**

| Byte | 内容 |
|---|---|
| 0–1 | 残容量 [mAh]（Little Endian） |
| 3 | 残量 [%] |

**内部処理**
- remaining_mah は **モジュール数分を乗算**して publish
- remaining_percent はそのまま使用

---

#### 5.2 モジュール IV フレーム

| 項目 | 内容 |
|---|---|
| CAN ID | `module_iv_ids[i]` |
| DLC | 4 byte 以上 |

**Payload 定義**

| Byte | 内容 |
|---|---|
| 0–1 | 電流 raw |
| 2–3 | 電圧 raw |

**変換式**
```
current[A] = (raw - 0x8000) * 0.01119
voltage[V] = raw * 4.8832 / 1000
```

---

### 6. パラメータ設定（YAML）

#### 最小構成例
```yaml
/**:
  ros__parameters:
    id_soc: 0x053
    module_iv_ids: [0x056, 0x076]
    pack_topology: series
```

#### パラメータ一覧

| パラメータ名 | 説明 |
|---|---|
| `rx_topic` | CAN 受信トピック |
| `battery_topic` | 出力トピック |
| `id_soc` | SOC 用 CAN ID |
| `module_iv_ids` | 各モジュールの IV 用 CAN ID |
| `pack_topology` | series / parallel |
| `parallel_voltage_method` | avg / max / min / first |

---

### 7. パック電圧算出ルール

#### 直列（series）
```
total_voltage = 各モジュール電圧の合計
```

#### 並列（parallel）
```
total_voltage = 代表電圧
```

代表電圧は `parallel_voltage_method` により決定。

---

### 8. 実行方法

```bash
colcon build --packages-select triorb_battery_info
source install/setup.bash

ros2 run triorb_battery_info battery_status \
  --ros-args --params-file /ws/params/battery_parallel.yaml
```

---

### 9. 動作仕様・注意点

- モジュール数 1 個でも動作可能
- `module_iv_ids` が空の場合、ノードは起動失敗
- DLC 不足の CAN フレームは無視
- タイムアウトによる無効化処理は未実装
- pack_topology は全モジュール共通前提

---

### 10. 内部設計メモ（社内向け）

- モジュール数は `module_iv_ids` のサイズから自動決定
- ID → モジュール index は起動時に固定マッピング
- パラメータは起動時のみ反映（動的変更なし）

---

### 11. 更新履歴

| 日付 | 内容 |
|---|---|
| 2025-xx-xx | 初版作成 |

---

### 12. 担当・関連

- 担当チーム：TriOrb Robotics Software
- 関連モジュール：CAN Bridge / Power Controller

