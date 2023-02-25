from datetime import datetime
import requests
import shutil
import sys
import os

RAW_URL_BASE = r"https://raw.githubusercontent.com/gental-py/dash2/main/"
DASH_PATH = r".\\"
OLD_DASH_PATH = DASH_PATH + "old\\"


def get_update_structure():
    structure_file_url = RAW_URL_BASE + ".update"

    response = requests.get(structure_file_url, timeout=5)
    if not response.status_code in range(200, 300):
        print(f"[ERROR]: .update file returned invalid status code: {response.status_code}")
        sys.exit(1)

    return response.json()

def download_file(url, local_path):
    file = requests.get(url, allow_redirects=True)
    local_path = os.path.abspath(local_path)

    try:   
        open(local_path, 'wb').write(file.content)
    except Exception as error:
        print(f"[ERROR]: Cannot download file: {error}")
        sys.exit(1)

def download_new_version():
    structure = get_update_structure()[""]

    def _handle_part(dir_name: str,structure: dict, path=DASH_PATH, web_path=""):
        dir_path = path + dir_name + "\\"
        web_path += dir_name + "/"

        if dir_name != "" and not os.path.exists(dir_path):
            os.mkdir(dir_path)

        files = structure["f"]
        for file in files:
            web_url = RAW_URL_BASE + web_path + file
            download_file(web_url, dir_path+file)
        
        dirs = structure["d"]
        for dir in dirs:
            _handle_part(dir, structure["d"][dir], dir_path, web_path)
        
    _handle_part("", structure)

def make_update(old_version: str, open_after_update=True):

    # Test internet connection.
    try:
        requests.get("https://example.com/", timeout=3)

    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        print("[ERROR]: No internet connection.")
        sys.exit(1)

    # Check old dash dir.
    if not os.path.exists(OLD_DASH_PATH):
        os.mkdir(OLD_DASH_PATH)

    # Create subdir for current version of dash.
    current_time = datetime.now().strftime("%H_%M_%S")
    subdir_name = f"{old_version} {current_time}\\"
    subdir_path = OLD_DASH_PATH + subdir_name
    if not os.path.exists(subdir_path):
        os.mkdir(subdir_path)
    
    # Move old dash version to it's subdir.
    for item in os.listdir("."):
        if item in ("updater.py", "old"): continue
        shutil.move(item, OLD_DASH_PATH + subdir_name)

    # Download all files and directories.
    download_new_version()

    print("update done.")

    if open_after_update:
        import dash
