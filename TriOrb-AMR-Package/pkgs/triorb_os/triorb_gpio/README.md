# triorb_gpio

このパッケージは、AMRに搭載されたGPIOインターフェースを通じて、外部デバイス（例：ランプ、ブザー、リレーなど）を制御するノードを提供します。

## 主な機能

- 外部信号出力（ブザー、警告灯）
- GPIOトリガによる動作制御
- エラー通知とログ

## 利用可能なGPIOピン
```
7,11,12,13,15,16,18,22,29,31,32,33,35,36,37,38,40
```

## 設定の保存
GPIOの入出力モード設定は、`/params/gpio.yaml`ファイルに保存されます。出力ピンのHi/Lo状態は保存されません。

---

## Subscriber
### GPIOの入出力モード設定（複数）
- Topic: /gpios/set_direction
- Type: std_msgs/msg/Int8MultiArray
- Values: -2: NotSet, -1: None, 0: Output, 1: Input
- Usage: 
```bash
# pin 37を非管理、pin 38を入力、pin 40を出力、その他は変更なしに設定
root@agx-orin-XXXX:/ws# ros2 topic pub -1 /gpios/set_direction std_msgs/msg/Int8MultiArray 'data: [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-1,1,0]'
```

### GPIOの出力値設定（複数）
- Topic: /gpios/set_value
- Type: std_msgs/msg/Int8MultiArray
- Values: -2: NotSet, -1: NotSet, 0: Low, 1: High
- Usage:
```bash
# pin 40をHighに、その他は変更なし
root@agx-orin-XXXX:/ws# ros2 topic pub -1 /gpios/set_value std_msgs/msg/Int8MultiArray 'data: [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-1,-1,1]'
```

### Publisher
### GPIOのHi/Lo値（複数）
- Topic: /gpios/value
- Type: std_msgs/msg/Int8MultiArray
- Values: -1: None, 0: Low, 1: High
- Frequency: 1Hz + エッジトリガ