#!/bin/bash
BASE_DIR=$(pwd)

python gather_md.py

source /opt/ros/*/setup.bash &&\
cd ./submodules/TriOrb-AMR-Package/host_pkgs &&\
colcon --log-base /triorb/log/${ROS_DISTRO} build --symlink-install --build-base /triorb/build/${ROS_DISTRO} --install-base /triorb/install/${ROS_DISTRO} --allow-overriding $(ls -d TriOrb-ROS2-Types/*_interface | sed 's/TriOrb-ROS2-Types\///') &&\
cd ${BASE_DIR} &&\
cd ./submodules/TriOrb-AMR-Package/vm_pkgs &&\
colcon --log-base /triorb/log/${ROS_DISTRO} build --symlink-install --build-base /triorb/build/${ROS_DISTRO} --install-base /triorb/install/${ROS_DISTRO} &&\
cd ${BASE_DIR} &&\
source /triorb/install/${ROS_DISTRO}/setup.bash


echo "# ROS2 Packages"
_vars=($(ros2 pkg list | grep triorb_))
for i in ${_vars[@]}
do
    echo "- [$i]($(find ./TriOrb-AMR-Package -name "README.md" | grep -m1 $i/README.md))"
done

echo ""
echo "# ROS2 Interface list"
_vars=($(ros2 interface list | grep triorb_))
for i in ${_vars[@]}
do
    _pkg=(${i//// }[0])
    _pkg=$(echo "$_pkg" | sed -e 's/ //g') 
    _link=$(echo "$i" | sed -e 's/\///g' | tr '[:upper:]' '[:lower:]')
    echo "- [$i]($(find ./TriOrb-AMR-Package -name "README.md" | grep -m1 $_pkg/README.md)#$_link)"
done