# Package: triorb_sync_move_navi
複数のロボットによる協調移動ジョブを実行するパッケージ
## 機能
- 世界座標系におけるジョブの情報（Weypointリストを含むJob description）を受け取り、協調移動ジョブを実行開始、運用、管理する
- "荷物座標系"における各ロボットの位置姿勢の定義値から、ロボットへ設定送信する☑
- "荷物座標系"における各ロボットの位置姿勢の定義値から、荷物の最大速度を算出する☑
- 世界座標系における荷物の現在位置姿勢とWaypointで定義された位置姿勢との差分から、荷物の目標速度ベクトルを算出し、荷物の目標速度ベクトルを各ロボットへ送信する☑
- 世界座標系における各ロボットの現在位置姿勢をロボから受信し、荷物の現在位置姿勢を推定☑、上位へ送信する☑
- ジョブ開始からN秒経過したらロボットのモーター制御を押し当てモードへ変更する☑
- 荷物の現在位置姿勢からWaypointへの到達判定を行う☑
- 荷物の現在位置姿勢からWaypointリスト(＊)が空になったら完了通知を上位へ送信し、ジョブを終了する☑
- 何らかの条件で移動に失敗した場合は失敗通知を上位へ送信し、ジョブを終了する☑
- ジョブ終了時にロボットのモーター制御を連続速度モードへ変更する☑
## その他
### 関連pkg
- triorb_sync_drive (local)
  - 荷物中心からロボットへの相対姿勢をsubscribeする
  - 荷物の目標速度ベクトルをsubscribeする
  - 荷物速度をロボットの目標速度ベクトルに変換してpublishする
  - モータードライバのライフタイムをpublishする
  - 荷物の目標速度0の指示を受け取った時点で移動完了と見なし待機状態に移行する
    - 目標姿勢と荷物姿勢の小数点精度次第ではwaypoint_listの途中で終了する可能性もあるので変えたほうがいいかも
- triorb_drive_pico (local)
  - drive_modeをsubscribeし、変更完了報告をpublishする

### 暴走対策
- triorb_sync_driveは剛体グループとの相対姿勢を受け取った際に、triorb_drive_picoにライフタイム6秒を設定する
- いずれかのロボットの最新姿勢のtimestampが現在のtimestampから7秒以上遅れていた場合、通信できていないとして剛体グループ下のロボット全てに速度指示0を送り、ジョブを終了する
  - 通信できていないロボットはライフタイムで止まってくれるはず
- /sync_move_navi/stop/naviをsubscribeするとジョブを終了する

### 荷物姿勢の定義
- 荷物の初期姿勢と各ロボットの相対姿勢は、/sync_move_manager/start/naviをsubscribeした時点で決定される <br>
  - 正確には、drive_mode変更報告を受けた後に全てのロボットの/vslam/rig_tfをsubscribeしたとき
  - xy座標は各ロボットのxyの平均値から算出する
  - 角度は各ロボットのxyの差のarctan2で計算され（ロボット2台の場合）、ロボットの角度には依存しない
    - 仮にロボット座標が(0,0,0)と(1,0,0)の場合は0度、(0,0,0)と(0,1,0)の場合は90度になる
    - この前者と後者はsubscribしたjsonのrobotsの順番に対応しており、順番を逆にすると角度の正負が逆転する
- 荷物姿勢は、各ロボットの現在姿勢を荷物姿勢に変換したものの平均値から計算される
  - タイムスタンプによる重みづけは行っていない（多分やるべき）が、現在時刻より1秒以上遅い姿勢は除かれる

### タイムアウトの処理
- 動き出してから60秒経っても目標地点に到達できない場合、一度だけリトライする
- リトライ時は1つのロボット姿勢のみを参照して剛体姿勢を決定する
- 注意点として、現在仕様(8/14)では全てのwaypointを終了するまでに60秒経過すると失敗になる(経由地点に到着してもタイマーがリセットされない)

# Request
目標地点が1か所の場合 <br>
- routeは[goal_x, goal_y, goal_deg, tx, ty, tdeg, [vel_xy, vel_w]] <br>
  - vel_xyとvel_wは入力しなかった場合、vel_xy=0.5, vel_w=0.3となる
  - 入力する場合は両方に値を与える必要がある
```json
{
  "name": "sample_payload",
  "mode": "sync_move",
  "robots": ["LIFTER2","LIFTER1"],
  "route": [ -3.0, 3.0, 90.0, 0.01, 0.01, 1.0 ]
}
```
目標地点が複数の場合(弧を描くイメージだが、多分そこまでうまくいかない)
※2つ目のwaypointでは速度xy=0.1, w=0.3とゆっくりになるように指定している
```json
{
  "name": "sample_payload",
  "mode": "sync_move",
  "robots": ["LIFTER2","LIFTER1"],
  "waypoint_list": [
    [ 1.414, 1.414, 45.0, 0.1, 0.1, 5.0 ],
    [ 2.0, 2.0, 90.0, 0.01, 0.01, 1.0, 0.1, 0.3 ]
  ]
}
```

# Report
## 剛体姿勢報告
現在実行中のwaypointのindexとかあると良いかも
```json
{
  "name": "sample_payload",
  "x": 1.0,
  "y": 2.0,
  "deg": 90.0
}
```
## ジョブ結果
現在は全てsuccessか、全てfailedの2通り
```json
{
  "Hash1": "success",
  "Hash2": "success"
}
```



# 構成
## sync_move_navi_node
ROSノード

## SolidGroup
剛体グループ

## Navigator
ナビゲーション


# 上位
## triorb_sync_move_manager
### Publish <br>
- 完了・失敗報告
  - /sync_move_navi/result
  - std_msgs::msg::String

### Subscirbe <br>
- 開始指示
  - /sync_move_manager/start/navi
  - std_msgs::msg::String


# 下位
## triorb_sync_drive
## triorb_drive_pico