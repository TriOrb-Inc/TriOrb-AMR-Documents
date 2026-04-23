# triorb_snr_mux_driver

**パス**: `triorb_drive/triorb_snr_mux_driver`  
**説明**: SNR-MUXボードとシリアル通信し、音声再生状態・発進待ち時間などを ROS 2 トピックへ配信するドライバです。navigate / navigation_manager の停止・一時停止の遅延を音声再生と連動させます。

## Package: triorb_snr_mux_driver

#### ノード概要 (snr_mux_driver.py)
- 目的: PLC/RobotStatus/aux event/drive vector を集約し、LED/LCD/スピーカ/走行ランプを制御する。
- Node名: `snr_mux_driver` (内部は `_snr_mux_driver`、`ROS_PREFIX` 付与でプレフィックス対応)
- バージョン: `1.2.3`
- シリアル: `/dev/ttyUSB0` / 115200bps
- タイマ周期
  - 0.5s: 状態に応じた表示/音声/ランプ更新
  - 0.1s: AUXイベント処理
  - 0.1s: シリアル送信
  - 0.02s: シリアル受信

#### ROS I/F
- Subscribe
  - `/drive/std_vector2` (Float32MultiArray)
  - `/collab/drive/std_vector2` (Float32MultiArray)
  - `/aux/event` (String)
  - `/collab/aux/event` (String)
  - `/robot/status` (RobotStatus)
  - `/plc/basic_data/from_plc` (BasicDataFromPLC)
  - `/plc/app_data/from_plc` (AppDataFromPLC)
  - `/plc/estop_detail/from_plc` (EstopDetailFromPLC)
  - `/battery/status` (BatteryStatus)
- Publish
  - `/except_handl/node/add` (String)
  - `/triorb/error/str/add` (String)
  - `/triorb/warn/str/add` (String)
- Service
  - `/get/version/snr_mux_driver` (Version)

#### AUXイベント (String)
- `start_move`, `start_collab_move`, `start_action`, `start_tag_navi`, `start_collab_lift`
- `pause`, `resume`, `collab_resume`, `stop`
- `nav_failed`, `reset`, `finish`, `collab_finish`
- `switch_to_collab`, `move_started`, `abnormal_occurred`, `abnormal_cleared`
- `/aux/event` は `nav_failed&&<num>` 形式で失敗理由番号を指定可能

#### 状態遷移
- 状態: `IDLE`, `TASK_EXECUTING`, `STANDARD_AUTO_MOVE_START`, `COLLAB_AUTO_MOVE_START`,
  `STANDARD_AUTO_MOVING`, `COLLAB_AUTO_MOVING`, `STANDARD_AUTO_MOVE_FAIL`,
  `COLLAB_AUTO_MOVE_FAIL`, `PAUSING`, `ERROR`
- `abnormal_occurred` で `ERROR`、`abnormal_cleared` で `IDLE` に戻る
- `reset` は `*_AUTO_MOVE_FAIL` から `PAUSING` へ遷移

#### 表示/音声の基本動作
- LCDは1行目に `Battery: xxx%`、2行目に状態文字列を表示 (改行区切りは `||`)
- エラー時は内容を2秒ごとにローテーション表示
- 走行ランプは `TAG_NAVI` 実行時のみ点灯
- 代表的な状態表示
  - `IDLE`: 待機/充電/モード選択に応じて表示
  - `TASK_EXECUTING`: 自律走行中 or TagSLAM 実行中
  - `*_AUTO_MOVE_*`: 走行中/開始中/失敗を色と音で通知
  - `ERROR`: 非常停止/リモートSW無効/カメラ/モータECU異常を優先表示

#### Drive Vector 取り扱い
- `std_vector2` の `data[2]` (角速度) が閾値超過で回転表示
- `data[0]` は 45度刻みで LED 方向に変換
- `data[1]` が移動閾値未満の場合は方向更新しない

#### エラー番号 / 音声番号一覧
- エラー種別 (表示文字列)
  - `SWITCH_PUSHED`: "Emergency Stop"
  - `REMOTE_SW_DISABLED`: "Remote SW || Disabled"
  - `CAMERA_ERROR`: "Camera Error"
  - `MOTOR_ECU_ERROR`: "Motor ECU Error"
- Nav失敗コード (`/aux/event` の `nav_failed&&<num>`)
  - 0: TIMEOUT_FAILED
  - 1: HALF_TIMEOUT
  - 2: TRANSFORM_FAILED
  - 3: NO_CHANGE_TIMESTAMP
  - 4: FORCE_STOP
  - 5: NAVIGATION_FAILED
  - 6: NAVIGATION_SUCCESS
  - 7: PROGRESS
  - 8: FORCE_SUCCESS
  - 9: LOST_FAILED
  - 255: REJECT
- 音声番号 (Speaker playlist)
  - 0: default
  - 1: start
  - 2: melody
  - 3: emergency (OBSTACLEと同値)
  - 4: error
  - 5: lost
  - 6: ecu_error
  - 9: charging
  - 12: nav_failed

#### pico-jetson間通信フォーマット
- SOF(2) | LEN(1) | ID(1) | SEQ(1) | PAYLOAD(N) | CRC16(2)
  - SOF: 0xAA55
  - LEN: ID+SEQ+PAYLOADの長さ
  - ID: Frame_ID
  - SEQ: 連番(0-255)
  - PAYLOAD: データ本体
  - CRC16: CRC16

#### Frame_ID 一覧
- 0xE1: watchdog
- 0xA1: IMU data
  - float array [yaw, pitch, roll, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]
- 0xA5: LED control
  - uint8_t array [light mode, bright level, flash setting, color id]
- 0xAA: LAMP control(走行ランプ)
  - uint8_t on/off
- 0xB1: LCD control
  - char array [表示文字列、15文字×4行] (改行記号"||")
- 0xB5: Speaker control
  - uint8_t array [play mode, playlist num, volume]
- 0xC1: LED/LCD/Speaker同時制御
  - json形式で各モジュールの制御データをまとめて送信
- 0xD1: 電源基盤からのinfo
  - uint8_t array [emg sw, cur over, pwr down, battery low, battery capa level]
- 0xD5: エラーステート通知
  - uint8_t array [error code]
- 0xE5: リブート指令
  - uint8_t arr追加 [0xE4, 0xFE, 0xFE]

#### 通信payload 詳細
- LED control (ID 0xA5)
  - light mode
    - 0: 消灯
    - 1: 全灯
    - 2: 全灯点滅     [有:点滅速度]
    - 3: 前進         [有:点滅速度]
    - 4: 右斜前       [有:点滅速度]
    - 5: 右           [有:点滅速度]
    - 6: 右斜後       [有:点滅速度]
    - 7: 後進         [有:点滅速度]
    - 8: 左斜後       [有:点滅速度]
    - 9: 左           [有:点滅速度]
    - 10: 左斜前      [有:点滅速度]
    - 11: 時計回り    [有:点滅速度]
    - 12: 反時計回り  [有:点滅速度]
  - bright level (明るさ)
    - 0x0000(min) ~ 0x0FFF(max)
  - flash setting (点灯速度)
    - 0: slow
    - 1: medium
    - 2: fast
    - 3: very fast
  - color id
    - 0:White
    - 1:blue
    - 2:Green
    - 3:red
    - 4:yellow
    - 5:violet
    - 6:magenda
    - 7:Black
- Speaker control (ID 0xB5)
  - play mode
    - 0: loop
    - 1: play once
    - 2: stop
  - playlist num
    - 0-255: あらかじめ登録された音源番号
  - volume
    - 0x00(min) ~ 0x3E(max)
- LAMP contorl (ID 0xAA)
  - on/off [0x00/0x01]
- Reboot control (ID 0xE5)
  - [0xE4, 0xFE, 0xFE]
- AUX total control (ID 0xC1)

#### 登録音声リスト(wavファイル)
No0 0000_sound_test: 動作確認用
No1 0001_auto-start: 「発進します」
No2 0002_warning_whistle_loop: 自律走行中の警告音
No3 0003_emergency: 「非常停止中です」
No4 0004_amr-move-error: 「AMR動作異常です」
No5 0005_amr-lost: 「ロストしました」
No6 0006_amr-motor-connect-err: 「AMR モータ制御接続ECU異常です」
No7 0007_lost-recover: 「ロスト復旧しました」
No8 0008_emg: 「非常停止が押されました」
No9 0009_charge_battery: 「充電中です」
No10 0010_battery_level_low: 「バッテリーレベルが低下しました」
No11 0011_tag_slam: 「tag slam実行中です」

