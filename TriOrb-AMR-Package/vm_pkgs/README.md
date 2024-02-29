[../](../README.md)
# TriOrb-AMR-Package on VM

## docker run
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

## build & install in docker container
```bash
source /ros_entrypoint.sh
# --allow-overridingを付けるとrebuildが遅くなるので注意
colcon --log-base /log/${ROS_DISTRO} build --symlink-install --build-base /build/${ROS_DISTRO} --install-base /install/${ROS_DISTRO} --allow-overriding $(ls -d TriOrb-ROS2-Types/*_interface | sed 's/TriOrb-ROS2-Types\///') &&\
source /install/${ROS_DISTRO}/setup.bash
```

## run
```bash
echo 'ROS_DISTRO='${ROS_DISTRO}', ROS_LOCALHOST_ONLY='${ROS_LOCALHOST_ONLY}', ROS_DOMAIN_ID='${ROS_DOMAIN_ID}', ROS_PREFIX='${ROS_PREFIX} &&\
ros2 launch release.xml
```