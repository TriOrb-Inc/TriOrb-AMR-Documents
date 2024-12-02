# Package: triorb_job_scheduler
- Taskの順序管理及び実行を行うパッケージ
- 制御フローは以下の通り
    1. スケジュールの新規開始を受け付ける（実行順、ループ回数）
    2. Task名に基づきJobを新規発行する
    3. Jobのresultを待ち、successが返ってきたら次のJobを発行する、その他であればスケジュールを終了する
    4. スケジュール終了要求があった場合は即座にJob中断リクエストを発行し、スケジュールを終了する
    5. なおStatusが一定期間（NO_STATUS_TIMEOUT）届かない場合はTimeoutと判断し即座にJob中断リクエストを発行し、スケジュールを終了する

## Subscription
### Jobスケジュールの新規開始
- Topic: (prefix)/fleet/schedule/new
- Type: std_msgs/msg/String
- Note: 既に実行中のスケジュールがある場合は即時中断されるため注意
- Note: loopする場合は'loop'のvalueにloop回数を設定する(0としも1回は実行される)
- Usage: 
```bash
root@orin-nx-4260:/ws# ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 99,\
    "'"task"'" : \
    [\
        "'"sample_task_01"'",\
        "'"sample_task_02"'",\
        "'"sample_task_03"'"\
    ]\
}'}"
```

### Jobスケジュールの中断終了
- Topic: (prefix)/fleet/schedule/terminate
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-4260:/ws# ros2 topic pub -1 /fleet/schedule/terminate std_msgs/msg/Empty
```

### [JobのResult](../../triorb_collaboration/triorb_job_state_manager/README.md#剛体グループjobのresult)

## Publisher
### [Jobの開始](../../triorb_collaboration/triorb_collab_find_workers/README.md#jobの開始要求)

### [現在実行中のJob（剛体グループ）を終了削除する](../../triorb_collaboration/triorb_job_state_manager/README.md#剛体グループjobを終了削除する)

## Service client
### [Task descriptionの取得](../triorb_task_library/README.md#task-descriptionの要求)

## Parameter
- NO_STATUS_TIMEOUT : ステータスが返ってこない場合にタイムアウト判断する時間 [ms]