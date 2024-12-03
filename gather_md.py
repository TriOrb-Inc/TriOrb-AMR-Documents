import subprocess
import glob
import os
import shutil
import pprint

submodule_root = "./submodules/"

# TriOrb-AMR-Static
#subprocess.run(f"git submodule update --init --recursive".split())
#subprocess.run(f"git submodule update --recursive --force --checkout --remote".split())

# Gather
copy_files = {}
for curDir, dirs, files in os.walk(submodule_root):
    files = [_f for _f in files if (_f.endswith('.md') or _f.endswith('.ipynb'))]
    files = [_f for _f in files if not _f.startswith('.')]
    files = [_f for _f in files if not _f.startswith('_')]
    copy_files.update({os.path.join(curDir, _f):os.path.join(curDir, _f).replace(submodule_root,"") for _f in files})

for src, dst in copy_files.items():
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"{src} > {dst}")

