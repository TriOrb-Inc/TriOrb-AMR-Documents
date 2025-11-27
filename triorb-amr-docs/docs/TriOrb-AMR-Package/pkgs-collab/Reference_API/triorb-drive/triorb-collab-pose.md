# triorb_collab_pose

**パス**: `triorb_drive/triorb_collab_pose`  
**説明**: センサフュージョン（拡張カルマンフィルターなど）により、AMR自身と荷物中心の姿勢を推定する協調ポーズ推定パッケージです。

## Package: triorb_collab_pose

このパッケージは、拡張カルマンフィルターなどのセンサフュージョン技術を用いて、AMR自身および協調搬送中の荷物の中心位置を推定します。

### 主な機能

- AMRの自己位置推定
- 複数ロボットからの情報統合
- 荷物中心位置の推定と共有

---

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

