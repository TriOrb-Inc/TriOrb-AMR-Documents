# triorb_gamepad

**パス**: `triorb_sensor/triorb_gamepad`  
**説明**: TODO: Package description

## Package: triorb_gamepad

### 概要
TriOrb AMR を市販/専用ゲームパッドから安全に操作する ROS 2 ノードを提供するパッケージです。`/dev/input/js*` を監視して対応デバイスを自動検出し、JSON で定義されたボタン/スティック割り当てに従って走行・リフタ・非常停止などのコマンドを生成します。ノード名やトピック名は `ROS_PREFIX` 環境変数を先頭に付与して重複を避けます。

### 提供ノード
#### `gamepad`
- `src/triorb_gamepad.cpp` の `_Node` クラスとして実装される単一ノードです。`UNIQUE_NODE` が有効なため同一名ノードが複数起動すると自動終了し、例外通知トピックへ状態を送出します。
- `dev` パラメータが空のときは `/dev/input/js0..js15` をスキャンして最初に反応したゲームパッドを使用します。
- ゲームパッド情報（名称・軸数・ボタン数）を読み込み、ユーザー辞書または `share/triorb_gamepad/params` のプリセットからマッピング設定を決定します。
- イベントループでは `AMRCtrl` 構造体に速度/加減速/リフタ状態を蓄積し、変化が生じたときのみ TriOrb RunVel コマンドを発行します。

##### モード管理
- 1 秒周期の `mode_check_timer` で購読者数を確認し、`/collab/wakeup` トピックに購読者がいる場合は「コラボレーションモード」に自動切替します。以後のコマンドは `/collab/...` 系トピックへ送出されます。
- `safe_run_mode` は `safe_drive/run_vel` もしくは `/collab/safe_drive/run_vel` の購読者が存在するか、直前に SafeRun モードだったかで判定されます。安全速度トピックが有効な場合は通常の `/drive/run_vel` ではなく SafeRun トピックへ速度メッセージを発行します。
- `active`/`inactive` コマンドによりゲームパッドの有効状態を明示でき、アクティブでない場合は速度を常に 0 とし、矛盾した状態が続くとデバイスを切断して再初期化させます。

### 購読インターフェース（Subscriber）
本ノードは ROS 2 上で購読するトピックを持たず、Linux のジョイスティックデバイス `/dev/input/js*` を唯一の入力源とします。外部アプリケーションからソフトウェア的に入力を与えたい場合は、仮想ジョイスティックにイベントを書き込むことで擬似的に「Subscriber」へ publish できます。

#### 外部からの呼び出し例
以下は `evemu-play` を用いて `/dev/input/js0` にボタン押下イベントを送る例です。`triorb_gamepad` ノードは実ジョイスティックと同様にイベントを受信し、対応するコマンドを実行します。

```bash
sudo apt install evemu-tools
sudo evemu-record /dev/input/js0 > /tmp/js0.desc   # 事前にデバイス定義を保存（初回のみ）
sudo evemu-play /dev/input/js0 <<'EOF'
E: 0.000000 1 304 1   # ボタンID304(例: Aボタン)押下
E: 0.010000 0 0 0
E: 0.050000 1 304 0   # ボタンを離す
E: 0.060000 0 0 0
EOF
```

仮想デバイスを自作する場合は `uinput` を使う Python/C++ スクリプトで同様のイベントを送出できます。ジョイスティックの軸やボタン番号は README 下部に記載した JSON 辞書に合わせる必要があります。

### パラメータ
| 名称 | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `dev` | string | `""` | 使用するデバイスファイル（例: `/dev/input/js1`）。空の場合は自動検出。 |
| `dict` | string | `/params/gamepad` | ユーザー定義のゲームパッド辞書を格納するディレクトリ。存在しない場合はノードが作成します。 |
| `acc_min` | int | `50` | `val_acc`/`val_dec` コマンドで生成される最小加速度 [ms]。 |
| `acc_max` | int | `10000` | 同最大加速度 [ms]。 |
| `vel_xy_min` | double | `0.0006` | 並進速度の最小値 [m/s]。 |
| `vel_xy_max` | double | `0.6` | 並進速度の最大値 [m/s]。 |
| `vel_w_min` | double | `0.00175` | 角速度の最小値 [rad/s]。 |
| `vel_w_max` | double | `1.75` | 角速度の最大値 [rad/s]。 |

> `robot_config` を辞書ファイル内に記述した場合は、上記パラメータよりもファイル側の値が優先されます。

### 発行トピック
#### 走行関連（標準モード）
- `/drive/run_vel` (`triorb_drive_interface/msg/TriorbRunVel3`): 並進/回転速度と加減速設定。`safe_run_mode` が true の場合は代わりに `/safe_drive/run_vel` を使用。
- `/safe_drive/run_vel` (`triorb_drive_interface/msg/TriorbRunVel3`): SafeRun 対応先への速度通知。
- `/drive/stop` (`std_msgs/msg/Empty`): 非常停止（E-Stop）要求。
- `/drive/sleep` (`std_msgs/msg/Empty`): 走行停止＆スリープ。
- `/drive/wakeup` (`std_msgs/msg/Empty`): 走行再開。
- `/drive/run_lifter` (`std_msgs/msg/String`): `"up"`, `"down"`, `"stop"` を通知。
- `/drive/set_life_time` (`std_msgs/msg/UInt16`): 予備。現状コマンド割当は定義されていません。

#### 走行関連（コラボレーションモード）
`/collab/drive/stop`, `/collab/sleep`, `/collab/wakeup`, `/collab/run_lifter`, `/collab/set_life_time`, `/collab/run_vel`, `/collab/safe_drive/run_vel` を標準モードと同じメッセージ型で発行します。

#### 例外通知
- `/except_handl/node/add` (`std_msgs/msg/String`): ノード登録通知。
- `/triorb/error/str/add` (`std_msgs/msg/String`): デバイス欠如・読み取り失敗などの致命的エラーを通知。
- `/triorb/warn/str/add` (`std_msgs/msg/String`): ゲームパッドの状態異常による切断など非致命的事象。

本パッケージはサービス／アクションを提供しません。

### ゲームパッドコマンド一覧
JSON 辞書内で使用する `name` に応じて次の処理が実行されます。

| コマンド名 | 内容 |
| --- | --- |
| `val_x` / `val_y` / `val_w` | スティックの値を -1.0 〜 1.0 に正規化し、それぞれ `vx`, `vy`, `vw` に適用。 |
| `val_acc` / `val_dec` | 指定範囲にリニアマップして `acc`/`dec` [ms] を更新。 |
| `val_vxy` / `val_vw` | 並進 / 角速度の最大値にリニアマップ。 |
| `acc_inc`, `acc_dec`, `dec_inc`, `dec_dec` | 100 ms 単位で加減速を微調整。 |
| `vel_vxy_inc`, `vel_vxy_dec`, `vel_vw_inc`, `vel_vw_dec` | 0.05 m/s、0.157 rad/s 単位で速度比率を変更。 |
| `wakeup`, `sleep` | ステート遷移。`sleep` 後は速度が 0 に固定。 |
| `lift_up`, `lift_down`, `lift_stop` | リフタ制御文字列を生成。連続押下は無視。 |
| `e_stop` | 押下時に `/drive/stop`（コラボ時は `/collab/drive/stop`）を即時発行。 |
| `active`, `inactive` | デバイスの状態監視に利用。アクティブでない場合は絶対に速度を出力しません。 |

コマンドに該当しない名称はログに `[Unknown cmd_name]` として出力されます。

### ゲームパッド辞書ファイル
- ファイル名は `<デバイス名>_<軸数>_<ボタン数>.json` とし、`dict` で指定したディレクトリ、または `share/triorb_gamepad/params` に配置します。例: `Generic X-Box pad_8_11.json`。
- 典型的な構造:

```json
{
  "name": "Generic X-Box pad",
  "axis_count": 8,
  "button_count": 11,
  "axis_cmds": [
    {"name": "val_x", "type": "analog", "min": -32767, "max": 32767},
    {"name": "val_y", "type": "analog", "min": 32767, "max": -32767},
    {"name": ["acc_dec", "dec_dec"], "type": "digital"}
  ],
  "button_cmds": [
    {"name": "lift_stop", "type": "digital"},
    {"name": ["vel_vxy_inc", "vel_vw_inc"], "type": "digital"}
  ],
  "robot_config": {
    "acc_min": 50,
    "acc_max": 10000,
    "vel_xy_min": 0.05,
    "vel_xy_max": 0.6,
    "vel_w_min": 0.1,
    "vel_w_max": 1.75
  }
}
```

- `axis_cmds`/`button_cmds` の要素数はデバイスが持つ軸・ボタン数と同じである必要があります。`name` を配列にすると 1 つの軸/ボタンに複数コマンドを割り当てられます。「未使用」は空文字列 `""` を指定してください。
- `type` が `analog` の場合は `min`/`max` を必ず設定します。`digital` の場合は押下時 (`value > 0`) にのみ実行されます。

### 利用手順
1. TriOrb ワークスペースで依存関係を満たした状態にし、`colcon build --packages-select triorb_gamepad` でビルドします。
2. ゲームパッドを接続し、必要であれば `~/.ros/gamepad` などの辞書格納先を用意し JSON を配置します。
3. `ros2 run triorb_gamepad triorb_gamepad --ros-args -p dict:=/home/robot/.ros/gamepad -p dev:=/dev/input/js0` のように実行します。
4. 起動時ログにデバイス名と割り当てが表示されます。意図したコマンドが発行されない場合は `axis_cmds`/`button_cmds` を確認してください。

### エラー時の挙動
- デバイスが見つからない／読み込み中に `ENODEV`/`EIO` が発生した場合は `_Node` が終了し、例外トピックに詳細を投稿します。
- 連続して不正値が送られ `need_disconnect()` が true になった場合は警告を発しデバイスを閉じて再検出します。
- ROS 2 ランタイムに致命的なエラーが無い限り、例外発生後も 1 秒待機して再接続を試みます。

