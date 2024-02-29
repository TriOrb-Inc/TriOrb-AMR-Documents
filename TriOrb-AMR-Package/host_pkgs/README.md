[../](../README.md)
# TriOrb-AMR-Package on Host
TriOrb AMRのための自律移動パッケージのうちOS起動と同時に実行するパケージ

# Packages
## [triorb_os_setting](./triorb_os_setting/README.md)
## [triorb_node_manager](./triorb_node_manager/README.md)
## [triorb_camera_capture](./triorb_camera_capture/README.md)
## [triorb_project_manager](./triorb_project_manager/README.md)

# Types
## [triorb_static_interface](./TriOrb-ROS2-Types/triorb_static_interface/README.md)
## [triorb_sensor_interface](./TriOrb-ROS2-Types/triorb_sensor_interface/README.md)
## [triorb_cv_interface](./TriOrb-ROS2-Types/triorb_cv_interface/README.md)
## [triorb_drive_interface](./TriOrb-ROS2-Types/triorb_drive_interface/README.md)
## [triorb_field_interface](./TriOrb-ROS2-Types/triorb_drive_interface/README.md)
## [triorb_project_interface](./TriOrb-ROS2-Types/triorb_project_interface/README.md)


# Develop
## install ros2 foxy [Ref](https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html)
```bash
sh foxy_install.sh
```

## ros2 setup
```bash
export ROS_LOCALHOST_ONLY=$(cat /triorb/params/ROS_LOCALHOST_ONLY)
export ROS_DOMAIN_ID=$(cat /triorb/params/ROS_DOMAIN_ID)
export ROS_PREFIX=$(cat /triorb/params/ROS_PREFIX)
source /opt/ros/foxy/setup.bash
```

## create new python package
```bash
python new_pkg_py.py -h
#python new_pkg_py.py triorb_new_package new_node
```

## create new cpp package
```bash
python new_pkg_cpp.py -h
#python new_pkg_cpp.py triorb_new_package new_node
```

## build & install
```bash
export ROS_LOCALHOST_ONLY=$(cat /triorb/params/ROS_LOCALHOST_ONLY)
export ROS_DOMAIN_ID=$(cat /triorb/params/ROS_DOMAIN_ID)
export ROS_PREFIX=$(cat /triorb/params/ROS_PREFIX)
source /opt/ros/foxy/setup.bash
# --allow-overridingを付けるとrebuildが遅くなるので注意
colcon --log-base /triorb/log/${ROS_DISTRO} build --symlink-install --build-base /triorb/build/${ROS_DISTRO} --install-base /triorb/install/${ROS_DISTRO} --allow-overriding $(ls -d TriOrb-ROS2-Types/*_interface | sed 's/TriOrb-ROS2-Types\///') &&\
source /triorb/install/${ROS_DISTRO}/setup.bash
```

## run
```bash
echo 'ROS_DISTRO='${ROS_DISTRO}', ROS_LOCALHOST_ONLY='${ROS_LOCALHOST_ONLY}', ROS_DOMAIN_ID='${ROS_DOMAIN_ID}', ROS_PREFIX='${ROS_PREFIX} &&\
ros2 launch release.xml
```