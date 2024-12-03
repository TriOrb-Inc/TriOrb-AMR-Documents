# Package: triorb_navigation

## 更新履歴
### 1.1.0
- forceのモード追加. bitフラグで指定できるように変更.
    - 回転のみモード追加
    - 並進のみモード追加
    - 速度指示モード追加(要調整)
    - 事後フィードバック制御モード追加
- 無フィードバック制御版が必ず失敗になっていたバグ修正
- 速度指示用のPIDパラメータ追加
- lookup_transformの参照先(robot)にprefixを追加
  - ROS_LOCALHOST_ONLY=0のロボットが複数いる場合に別ロボットの姿勢を参照することがある問題の対策のため
- 速度指示モードではlifetimeを設定


## 動作モード(forceフラグ)
各bitの組合せで指定
- フィードバック制御フラグ(0b00000001)
    - 0でフィードバック制御しない
    - 1でフィードバック制御する
    - 速度指示モードと事後フィードバック制御モードでは無効
- 事後フィードバック制御フラグ(0b00000010)
    - フィードバック制御しない場合、移動完了後にフィードバック制御を行う
    - おおまかに位置決めした後に精密位置合わせしたい場合に使用
- 回転モードフラグ(0b00001000)
    - 並進指示値が常に0になり、並進方向の精度を無視する
    - 並進モードフラグと併用できない（移動しないが常に成功判定になる）
- 並進モードフラグ(0b00010000)
    - 回転指示値が常に0になり、回転方向の精度を無視する
    - 何らかの原因でロボットが回転した場合でも元の角度に復帰することはない
    - 回転モードフラグと併用すると正常に動作しない
- 速度指示モード(0b10000000)
    - 速度指示モードになり、見た目上なめらかに動く
    - フィードバック制御フラグに関わらずフィードバック制御を行う

## Subscriber
### 自律移動を終了する
- Topic: (prefix)/drive/stop
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/stop std_msgs/msg/Empty 
```

### 世界座標系目標位置指示による移動 
- Topic: (prefix)/drive/set_pos
- Type: triorb_drive_interface/msg/TriorbSetPos3
- Usage: 
```bash
```
### 自律移動時のPIDゲインを設定する
- Topic: (prefix)/setting/drive/gains
- Type: triorb_drive_interface/msg/DriveGains
- Usage: 
```bash
```

## Publisher
### 移動距離指示による相対移動
- Topic: (prefix)/drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage: 
```bash
```
### 自律移動完結果
- Topic: (prefix)/drive/result
- Type: triorb_drive_interface/msg/TriorbRunResult
- Usage: 
```bash
```

## Service
### 世界座標系目標位置指示による移動（移動完了結果報告あり） 
- Topic: (prefix)/srv/drive/set_pos
- Type: triorb_drive_interface/srv/TriorbSetPos3
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /srv/drive/set_pos \ 
triorb_drive_interface/srv/TriorbSetPos3 "{pos: { setting: { tx: 0.01, ty: 0.01, tr: 1.0, force: 1} , pos: {speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, position: {x: 0.6037, y: 0.3599, deg: 0.3176}}}}" 
# コマンド以上 

waiting for service to become available... 
requester: making request: 
triorb_drive_interface.srv.TriorbSetPos3_Request(pos=triorb_drive_interface.msg.TriorbSetPos3(pos=triorb_drive_interface.msg.TriorbRunPos3(speed=triorb_drive_interface.msg.TriorbSpeed(acc=500, dec=500, xy=0.1, w=0.0), position=triorb_drive_interface.msg.TriorbPos3(x=0.6037, y=0.3599, deg=0.3176)), setting=triorb_drive_interface.msg.TriorbRunSetting(tx=0.01, ty=0.01, tr=1.0, force=1))) 

response: 
triorb_drive_interface.srv.TriorbSetPos3_Response(result=triorb_drive_interface.msg.TriorbRunResult(success=True, position=triorb_drive_interface.msg.TriorbPos3(x=0.5981971025466919, y=0.3542609214782715, deg=0.3284424841403961)))
```

## Action
### 世界座標系目標経路指示による移動（途中経過、移動完了結果報告あり） 
- Topic: (prefix)/action/drive/set_path
- Type: triorb_drive_interface/action/TriorbSetPath
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 action send_goal /action/drive/set_path \ 
triorb_drive_interface/action/TriorbSetPath "{path: \ 
  [ \ 
    { \ 
      setting: {tx: 0.01, ty: 0.01, tr: 1.0, force: 1}, \ 
      pos: { \ 
        speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, \ 
        position: {x: 0.6033, y: 0.3756, deg: 0.3506} \ 
      } \ 
    }, \ 
    { \ 
      setting: {tx: 0.01, ty: 0.01, tr: 1.0, force: 1}, \ 
      pos: { \ 
        speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, \ 
        position: {x: 0.2765, y: -0.3236, deg: 0.7407} \ 
      } \ 
    }, \ 
    { \ 
      setting: {tx: 0.01, ty: 0.01, tr: 1.0, force: 1}, \ 
      pos: { \ 
        speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, \ 
        position: {x: 0.6033, y: 0.3756, deg: 0.3506} \ 
      } \ 
    } \ 
  ] \ 
}" --feedback 
# コマンド以上 

Goal accepted with ID: cd019fbfa70349789c87ea90fdd10239 

Feedback: 
    way_idx: 0 
now: 
  x: 0.6081861257553101 
  y: 0.38933515548706055 
  deg: 0.1585390269756317 
# ---- (フィードバック略) ---- 

Feedback: 
    way_idx: 2 
now: 
  x: 0.5898382663726807 
  y: 0.35128170251846313 
  deg: -0.009930066764354706 

Result: 
    result: 
  success: true 
  position: 
    x: 0.5965888500213623 
    y: 0.3684644103050232 
    deg: 0.07557345926761627 

Goal finished with status: SUCCEEDED 
```