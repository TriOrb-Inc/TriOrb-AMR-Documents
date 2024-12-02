# Package: triorb_relative_alignment
- マーカーを基準とした相対位置決め移動の実行

# Requirement definition
```bash
{
    acc : (加速時間 time [ms]), # 任意。設定が無ければプリセットを使う
    vel_xy_max : (ロボットの最大並進速度　[m/s]), # 任意。設定が無ければプリセットを使う
    vel_w_max : (ロボットの最大回転速度　[rad/s]), # 任意。設定が無ければプリセットを使う
    tags_pose : [
        {
            id : (tag id), # Tag1のID
            pose_goal2tag : [(x),(y),(yaw)] # Goal座標系におけるタグ1の位置・姿勢
        },
        {
            id : (tag id), # Tag2のID
            pose_goal2tag : [(x),(y),(yaw)] # Goal座標系におけるタグ2の位置・姿勢
        },
        {
            id : (tag id), # Tag3のID
            pose_goal2tag : [(x),(y),(yaw)] # Goal座標系におけるタグ3の位置・姿勢
        }
    ]
},
```

# Service
## 現在見えているタグの相対姿勢情報(robot2tags)を取得
- Service: (prefix)/drive/alignment/srv/get_tags
- Type: std_srvs/srv/Trigger
- Note: "タグ相対姿勢推定のみ開始"状態である必要がある
- Usage：
```bash
root@orin-nx-toda-1go:/ws# ros2 topic pub -1 /drive/alignment/start/detect_only std_msgs/msg/String
publisher: beginning loop
publishing #1: std_msgs.msg.String(data='')

root@orin-nx-toda-1go:/ws# ros2 service call /drive/alignment/srv/get_tags std_srvs/srv/Trigger
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='{"tags_pose": [{"id": "0", "pose_goal2tag": [0.42632964975188725, 0.0008492655958919461, -95.25343144714356]}, {"id": "1", "pose_goal2tag": [0.461662644243898, 0.14932690205624627, -165.66381987317297]}, {"id": "2", "pose_goal2tag": [0.44695366683212034, -0.13160227179054612, -24.916975273946008]}, {"id": "3", "pose_goal2tag": [-0.44885464336120595, -0.12584908094456257, 26.910205716541668]}, {"id": "4", "pose_goal2tag": [-0.4262322711278036, 0.005939190729071545, 95.860490833845]}, {"id": "5", "pose_goal2tag": [-0.4640556788419471, 0.16179577223981575, 166.58180851763746]}]}')
```


# Subscriber
## タグ相対姿勢推定のみ開始（ロボットは動かさない）
- Topic: (prefix)/drive/alignment/start/detect_only
- Type： std_msgs/msg/String
- Note：リクエスト文字列は一旦カラ
- Usage：
```bash
root@orin-nx-toda-1go:/ws# ros2 topic pub -1 /drive/alignment/start/detect_only std_msgs/msg/String
```

## 相対位置決め開始Request
- Topic: (prefix)/drive/alignment/start
- Type： std_msgs/msg/String
- Note：リクエスト文字列はjson形式
- Usage：
```bash
```

## 相対位置決め終了Request
- Topic: (prefix)/drive/alignment/terminate
- Type： std_msgs/msg/String
- Note：リクエスト文字列は一旦カラの予定


# Subscriber
## Tag検出の結果を受け取る
- Topic：(prefix)/relative_align_marker/transform
- Type：geometry_msgs/msg/TransformStamped
- Definition：カメラから見たマーカーの位置姿勢（右手系）
- Usage：
```bash
```

# Publisher
## Tag検出を開始する
- Topic：(prefix)/relative_align_marker/start
- Type：std_msgs/msg/Bool

## Tag検出を終了する
- Topic：(prefix)/relative_align_marker/stop
- Type：std_msgs/msg/Bool

## Robotに速度指示を送る
- Topic：(prefix)/drive/run_vel
- Type：TriorbRunVel3


# パラメーター
- ROBOT_VEL_MAX_TRANS : ロボットの最大並進速度 [m/s]
- ROBOT_VEL_MAX_ROT : ロボットの最大回転速度 [rad/s]
- PID_GAIN_TRANS_P : 並進用のP Gain
- PID_GAIN_TRANS_I : 並進用のI Gain
- PID_GAIN_TRANS_D : 並進用のD Gain
- PID_GAIN_ROT_P : 回転用のP Gain
- PID_GAIN_ROT_I : 回転用のI Gain
- PID_GAIN_ROT_D : 回転用のD Gain
- FAIL_SAFE_TIME : 移動指示をキャンセルする時間 [sec]
- ACC_TIME_MS：加減速時間 [ms]
- ONGOAL_ERROR_XY : 並進方向の許容誤差 [m]
- ONGOAL_ERROR_YAW : 回転方向の許容誤差 [deg]
- ONGOAL_VELOCITY_XY : 並進方向のゴール判定速度 [m/s]
- ONGOAL_VELOCITY_YAW : 回転方向のゴール判定速度 [rad/s]


# MEMO
## カメラデバイスの名前解決（docker起動前）
```bash
if [ ! -e /dev/video-usb0 ]; then
    sudo -E python /triorb/install/scripts/fix_video_device.py
fi
```

## dockerの起動
```bash
docker run -it --rm --name dev_local --privileged --net=host --ipc=host --pid=host --runtime=nvidia --gpus all \
            --add-host=localhost:127.0.1.1 \
            -e ROS_LOCALHOST_ONLY=1 \
            -e ROS_DOMAIN_ID=$(cat /triorb/params/ROS_DOMAIN_ID) \
            -e ROS_PREFIX=$(cat /triorb/params/ROS_PREFIX) \
            -v /triorb:/triorb \
            -v /dev:/dev \
            -v /sys/devices/:/sys/devices/ \
            -v /triorb/log:/log \
            -v /triorb/build:/build \
            -v /triorb/install:/install \
            -v /triorb/params:/params \
            -v /triorb/data:/data \
            -v /triorb/tslam:/tslam \
            -v /triorb/.jupyter:/root/.jupyter \
            -v /etc/NetworkManager/system-connections:/etc/NetworkManager/system-connections \
            -v /var/run/dbus:/var/run/dbus \
            -v $(pwd):/ws \
            -w /ws \
            $(cat /triorb/params/DOCKER_IMAGE_ROS) /bin/bash -c '\
                    source /ros_entrypoint.sh &&\
                    source /install/humble/setup.bash &&\
                    python3 -m pip install pupil_apriltags &&
                    /bin/bash'
```

## モーター制御Node、カメラキャプチャNode、タグ検出Node、の起動（docker内）
```bash
source /install/humble/setup.bash
tmux new-session -s camera -d "ros2 run triorb_camera_capture camera_capture --ros-args --param dev:=/dev/video-csi0,/dev/video-usb0,/dev/video-usb1,/dev/video-usb2 --param pub:=/camera0,/camera3,/camera4,/camera2 --param rot:=0,0,0,180"
tmux new-session -s stream_camera -d "ros2 run triorb_streaming_images streaming_image_node --port 3332 --ip "0.0.0.0" --ros-args --param topic_name_raw:=/camera0 --param sub_path:=/camera --param scale:=0.5 --param fps:=1.0"
tmux new-session -s drive -d "ros2 run triorb_drive_pico drive"

tmux new-session -s marker -d "colcon build --packages-select triorb_relative_align_marker && source ./install/setup.bash && ros2 run triorb_relative_align_marker relative_align_marker"

```

## 本Nodeの起動
```bash
tmux new-session -s align -d "colcon build --packages-select triorb_relative_alignment && source ./install/setup.bash && ros2 run triorb_relative_alignment relative_alignment"
```
