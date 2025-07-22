# Package: triorb_gpio
## GPIO番号（J401）
### J10 : 40-pin Expansion Header
GPIO pins: [7,11,12,13,15,16,18,22,29,31,32,33,35,36,37,38,40]

|Header Pin #|Module Pin Name|Module Pin #|SoC Pin name|Default Usage / Description|Alternate Functionality|Pin Drive or Power Pin Max Current|SoC GPIO Port #|
|:--:|:--|:--:|:--|:--|:--|:--|:--:|
|1|–|–|–|Main 3.3V Supply|–|1A|–|
|2|–|–|–|Main 5.0V Supply|–|1A|–|
|3|I2C1_SDA|191|DP_AUX_CH3_N|I2C #1 Data|–|±2mA|–|
|4|–|–|–|Main 5.0V Supply|–|1A|–|
|5|I2C1_SCL|189|DP_AUX_CH3_P|I2C #1 Clock|–|±2mA|–|
|6|–|–|–|Ground|–|–|–|
|7|GPIO09|211|AUD_MCLK|GPIO|Audio Master Clock|±20µA|PS.04|
|8|UART1_TXD|203|UART1_TX|UART #1 Transmit|GPIO|±20µA|PR.02|
|9|–|–|–|Ground|–|–|–|
|10|UART1_RXD|205|UART1_RX|UART #1 Receive|GPIO|±20µA|PR.03|
|11|UART1_RTS*|207|UART1_RTS|GPIO|UART #2 Request to Send|±20µA|PR.04|
|12|I2S0_SCLK|199|DAPS_SCLK|GPIO|Audio I2S #0 Clock|±20µA|PT.05|
|13|SPI1_SCK|106|SPI1_SCK|GPIO|SPI #1 Shift Clock|±20µA|PY.00|
|14|GPIO12|218|TOUCH_CLK|GPIO|–|–|–|
|15|SPI1_CS1*|112|SPI3_CS1|GPIO|SPI #1 Chip Select #1|±20µA|PCC.04|
|16|–|–|–|Main 3.3V Supply|–|±20µA|PY.04|
|17|SPI1_CS0*|110|SPI3_CS0|GPIO|SPI #0 Chip Select #0|1A|–|
|18|–|–|–|Ground|–|±20µA|PZ.05|
|19|SPI0_MOSI|89|SPI1_MOSI|GPIO|SPI #0 Master Out/Slave In|±20µA|PZ.05|
|20|–|–|–|Ground|–|–|–|
|21|SPI0_MISO|93|SPI1_MISO|GPIO|SPI #0 Master In/Slave Out|±20µA|PZ.04|
|22|SPI1_MISO|103|SPI1_MISO|GPIO|SPI #1 Master In/Slave Out|±20µA|PY.01|
|23|SPI0_SCK|91|SPI1_SCK|GPIO|SPI #0 Shift Clock|±20µA|PZ.03|
|24|SPI0_CS0*|95|SPI1_CS0|GPIO|SPI #0 Chip Select #0|±20µA|PZ.06|
|25|–|–|–|Ground|–|–|–|
|26|SPI0_CS1*|97|SPI1_CS1|GPIO|SPI #0 Chip Select #1|±20µA|PZ.07|
|27|I2C0_SDA|187|GEN2_I2C_SDA|I2C #0 Data|GPIO|±2mA|PDD.00|
|28|I2C0_SCL|185|GEN2_I2C_SCL|I2C #0 Clock|GPIO|±2mA|PCC.07|
|29|GPIO01|118|SOC_GPIO41|GPIO|–|±20µA|PQ.05|
|30|–|–|–|Ground|–|–|–|
|31|GPIO11|216|SOC_GPIO42|GPIO|General Purpose Clock #1|±20µA|PQ.06|
|32|GPIO07|206|SOC_GPIO44|GPIO|PWM|±20µA|PR.00|
|33|GPIO13|228|SOC_GPIO54|GPIO|PWM|±20µA|PN.01|
|34|–|–|–|Ground|–|–|–|
|35|I2S0_FS|197|DAPS_FS|GPIO|Audio I2S #0 Field Select|±20µA|PU.00|
|36|UART1_CTS*|209|UART1_CTS|GPIO|UART #1 Clear to Send|±20µA|PR.05|
|37|SPI1_MOSI|101|SPI1_MOSI|GPIO|SPI #1 Master Out/Slave In|±20µA|PY.02|
|38|I2S0_DIN|195|DAPS_DIN|GPIO|Audio I2S #0 Data in|±20µA|PT.07|
|39|–|–|–|Ground|–|–|–|
|40|I2S0_DOUT|193|DAPS_DOUT|GPIO|Audio I2S #0 Data Out|±20µA|PT.06|

### J401 - J10 : GPIOピンインデックス
|GPIO pin No|Index|
|:--:|:--:|
|7|0|
|11|1|
|12|2|
|13|3|
|15|4|
|16|5|
|18|6|
|22|7|
|29|8|
|31|9|
|32|10|
|33|11|
|35|12|
|36|13|
|37|14|
|38|15|
|40|16|

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
- Usage: 
```bash
root@agx-orin-XXXX:/ws# ros2 topic echo /gpios/value
layout:
  dim: []
  data_offset: 0
data:
- -1
- -1
- -1
- -1
- -1
- -1
- -1
- -1
- -1
- -1
- -1
- -1
- -1
- -1
- -1
- 1
- 0
---
```