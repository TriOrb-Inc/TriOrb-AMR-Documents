import subprocess
import glob
import os
import shutil
import pprint

submodule_root = "./submodules/"
dst_root = "./triorb-amr-docs/docs/"

# TriOrb-AMR-Static
#subprocess.run(f"git submodule update --init --recursive".split())
#subprocess.run(f"git submodule update --recursive --force --checkout --remote".split())

EXCLUDE_KWDS = [
    'triorb_stub_pico/',
    'tagslam_ws/src/flex_sync/',
    'tagslam_ws/src/tagslam/',
    'pkgs-collab/triorb_collaboration/',
    'pkgs/rosbridge_suite/',
    'cuda_efficient_features/',
    'TriOrb-AMR-Package/gui/',
    'stella_vslam_ros/README.md',
    'stella_vslam_ros/socket_publisher/',
    'stella_vslam_ros/doc/',
    'stella_vslam_ros/3rd/',
    'stella_vslam_ros/stella_vslam/',
    '.github/',
    'template/',
    'dev_tools/',
    'mqtt_client/',
    'calibration/',
    'MEMO.md',
    'ListOfOSS.md',
    'GuideForMaintainer.md',
    'CONTRIBUTING.md',
    'TriOrb-AMR-Package/README.md',
    'pkgs/triorb_navi_bridge/',
    'pkgs/triorb_os/',
    'pkgs/triorb_sensor/',
    'pkgs/triorb_drive/',
    'pkgs/tagslam_ws/',
    'pkgs/TriOrb-ROS2-Types/triorb_drive_interface/',
    'pkgs/stella_vslam_ros/',
    'pkgs/triorb_fleet/',
    'pkgs/triorb_service/',
    'pkgs-collab/triorb_drive/',
]

# Clean
dst_dires = [src.replace(submodule_root, dst_root) for src in glob.glob(os.path.join(submodule_root, '*'))]
subprocess.run(f"rm -rf {' '.join(dst_dires)}".split())

# Gather
copy_files = {}
for curDir, dirs, files in os.walk(submodule_root):
    files = [_f for _f in files if (_f.endswith('.md') or _f.endswith('.ipynb'))]
    files = [_f for _f in files if not _f.startswith('.')]
    files = [_f for _f in files if not _f.startswith('_')]
    copy_files.update({os.path.join(curDir, _f):os.path.join(curDir, _f).replace(submodule_root, dst_root) for _f in files})

for src, dst in copy_files.items():
    if any([exclude_kwd in dst for exclude_kwd in EXCLUDE_KWDS]):
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"{src} > {dst}")

