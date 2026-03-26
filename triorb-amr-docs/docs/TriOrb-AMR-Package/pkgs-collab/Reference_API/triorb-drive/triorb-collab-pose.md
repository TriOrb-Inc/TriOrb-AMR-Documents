# triorb_collab_pose

**パス**: `triorb_drive/triorb_collab_pose`  
**説明**: 拡張カルマンフィルターとTF平均化で各ロボットのバインド姿勢や協調グループ中心を推定し、TFを配信する協調ポーズ推定パッケージです。

## triorb_collab_pose

拡張カルマンフィルターとTF平均化で各ロボットのバインド姿勢や協調グループ中心を推定し、TFを配信する協調ポーズ推定パッケージです。

### Subscriber
#### VSLAMからの姿勢受信
- Topic: `/vslam/robot_pose`
- Type: `triorb_drive_interface::msg::TriorbPos3`

#### 各ロボットの姿勢受信
- Topic: `/bc/collab/robot_pose`
- Type: `triorb_drive_interface::msg::TriorbPos3Stamped`

#### バインド姿勢情報受信
- Topic: `/bc/collab/bind/info`
- Type: `triorb_collaboration_interface::msg::ParentBind`

### Publisher
#### VSLAMからの姿勢リパブリッシュ
- Topic: `/collab/robot_pose`
- Type: `triorb_drive_interface::msg::TriorbPos3Stamped`

#### 協調グループの姿勢リパブリッシュ
- Topic: `/collab/group_pose`
- Type: `triorb_drive_interface::msg::TriorbPos3Stamped`

### TransformBroadcaster
#### 協調グループの姿勢
- Child Frame ID: `${グループ名}`
- Parent Frame ID: `triorb_map`

