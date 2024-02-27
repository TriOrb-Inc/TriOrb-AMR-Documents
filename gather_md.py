import subprocess
import glob
import os
import shutil
import pprint

submodule_root = "./submodules/"

# TriOrb-AMR-Static
clone_dir = os.path.join(submodule_root, "TriOrb-AMR-Static")
shutil.rmtree(clone_dir)
subprocess.run(f"git clone --depth=1 git@github.com:TriOrb-Inc/TriOrb-AMR-Static.git {clone_dir}".split())

# Gather
copy_files = {}
for curDir, dirs, files in os.walk(submodule_root):
    files = [_f for _f in files if _f.endswith('.md')]
    copy_files.update({os.path.join(curDir, _f):os.path.join(curDir, _f).replace(submodule_root,"") for _f in files})
pprint.pprint(copy_files)
for src, dst in copy_files.items():
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(src, dst)