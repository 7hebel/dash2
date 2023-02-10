import re
import os

def get_all_disks():
    all_disks = [
        full_disk_name for full_disk_name in
        re.findall(
            r"[A-Z]+:.*$", os.popen("mountvol /").read(),
            re.MULTILINE
        )
    ]
    return all_disks

def list_dir(path):
    dirs, files = [], []
    for object in path.iterdir():
        if object.is_dir():
            dirs.append(object.name)
        if object.is_file():
            files.append(object.name)
    return dirs, files

def has_permissions(path):
    return os.access(path, os.R_OK) and os.access(path, os.W_OK)
