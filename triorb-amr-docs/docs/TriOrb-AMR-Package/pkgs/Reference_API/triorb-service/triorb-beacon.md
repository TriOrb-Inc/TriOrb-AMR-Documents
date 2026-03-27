# triorb_beacon

**パス**: `triorb_service/triorb_beacon`  
**説明**: ホストの IP・プレフィクス情報・グループ情報を定期的に配信

## triorb_beacon

端末の IP・プレフィクス情報を定期送信し、グループ情報も FastAPI から取得して配信します。

### Active API

#### 個体ビ―コン
- Topic：(prefix)/triorb/beacon2
- Node：(prefix)_triorb_beacon
- Type： std_msgs/msg/String
- Note：`{"hostname":"...","ip":"...","prefix":"..."}` JSON を 2 秒周期で publish
- Usage：
```
ros2 topic echo /triorb/beacon2
```

#### グループビ―コン
- Topic：(prefix)/group/beacon2
- Node：(prefix)_triorb_beacon
- Type： std_msgs/msg/String
- Note：FastAPI `fastapi_group_url` が成功した場合のみ `group` を追加して publish
- Usage：
```
ros2 topic echo /group/beacon2
```

