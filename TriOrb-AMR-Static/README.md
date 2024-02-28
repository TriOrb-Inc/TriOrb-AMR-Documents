# TriOrb-AMR-Static
TriOrb AMRのための自律移動パッケージのうちOS起動と同時に実行するパケージ

# Packages
## [triorb_os_setting](./triorb_os_setting/README.md)
## [triorb_node_manager](./triorb_node_manager/README.md)

# Types
## [triorb_static_interface](./TriOrb-ROS2-Types/triorb_static_interface/README.md)

# Develop
## [Setup] install ros2 foxy [Ref](https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html)
```bash
sh foxy_install.sh
```

## [Develop] ros2 run
```bash
export ROS_LOCALHOST_ONLY=$(cat /triorb/params/ROS_LOCALHOST_ONLY)
export ROS_DOMAIN_ID=$(cat /triorb/params/ROS_DOMAIN_ID)
export ROS_PREFIX=$(cat /triorb/params/ROS_PREFIX)
source /opt/ros/foxy/setup.bash
```

## [Develop] build on host & install
```bash
export ROS_LOCALHOST_ONLY=$(cat /triorb/params/ROS_LOCALHOST_ONLY)
export ROS_DOMAIN_ID=$(cat /triorb/params/ROS_DOMAIN_ID)
export ROS_PREFIX=$(cat /triorb/params/ROS_PREFIX)
source /opt/ros/foxy/setup.bash
colcon --log-base /triorb/log/${ROS_DISTRO} build --symlink-install --allow-overriding triorb_static_interface --build-base /triorb/build/${ROS_DISTRO} --install-base /triorb/install/${ROS_DISTRO}
source /triorb/install/${ROS_DISTRO}/setup.bash
```

## [Develop] run on host
```bash
sh launch.sh
```

# Packages
## - [triorb_os_setting](./triorb_os_setting/README.md)


# dockerコンテナでは実行不可（reboot / shutdownが不可能）
## [Develop] docker run
```bash
docker run -it --rm --name static --privileged --net=host --runtime=nvidia --gpus all \
               --add-host=localhost:127.0.1.1 \
               -e ROS_LOCALHOST_ONLY=$(cat /triorb/params/ROS_LOCALHOST_ONLY) \
               -e ROS_DOMAIN_ID=$(cat /triorb/params/ROS_DOMAIN_ID) \
               -e ROS_PREFIX=$(cat /triorb/params/ROS_PREFIX) \
               -v /dev:/dev \
               -v /sys/devices/:/sys/devices/ \
               -v /triorb/log:/log \
               -v /triorb/build:/build \
               -v /triorb/install:/install \
               -v /triorb/params:/params \
               -v /triorb/data:/data \
               -v /triorb/tslam:/tslam \
               -v /etc/NetworkManager/system-connections:/etc/NetworkManager/system-connections \
               -v /var/run/dbus:/var/run/dbus \
               -v $(pwd):/ws \
               -w /ws \
               $(cat /triorb/params/DOCKER_IMAGE_ROS)
```

## [Develop] build on docker & install
```bash
source /ros_entrypoint.sh
# --allow-overridingを付けるとrebuildが遅くなるので注意
colcon --log-base /log/${ROS_DISTRO} build --symlink-install --allow-overriding triorb_static_interface --build-base /build/${ROS_DISTRO} --install-base /install/${ROS_DISTRO}
source /install/${ROS_DISTRO}/setup.bash
```
