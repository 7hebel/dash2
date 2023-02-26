"""
Module: config.py
Contains default config and user config getter.
"""

import getpass
import json
import os

import Modules.display as Display

__defaults__ = {
    "prompt": "#gray[#white%cwd#gray] #blue#bold~ #reset",
    "osprefix": ".",
    "defaultdir": ".",
    "autoupdate": "0",
    "varsdump": "" 
}

CONFIG_DIR_PATH = f"/home/{getpass.getuser()}/.config/dash/"
CONFIG_FILE_PATH = CONFIG_DIR_PATH + "config.json"


def _set_defaults():
    with open(CONFIG_FILE_PATH, "a+", encoding="utf8") as file:
        json.dump(__defaults__, file, indent=4)
    Display.Message.warning("Something was wrong with config. Reseted.")
            
def _get_config_content():
    content = {}
    with open(CONFIG_FILE_PATH, "r", encoding="utf8") as file:
        content = json.loads(file.read())
    return content
    
def check_files():
    if not os.path.exists(CONFIG_DIR_PATH):
        os.mkdir(CONFIG_DIR_PATH)
        
    if not os.path.exists(CONFIG_FILE_PATH):
        _set_defaults()
        
    try:
        _get_config_content()
    except:
        _set_defaults()
            
def get_value(key):
    config = get_config()
    return config[key]

def set_value(key, value):
    new_content = _get_config_content()
    new_content.update({key: value})
    
    with open(CONFIG_FILE_PATH, "w+", encoding="utf8") as file:
        json.dump(new_content, file, indent=4, separators=(',',': ')) 
    
def get_config() -> dict:
    config = _get_config_content()
        
    for key, default_value in __defaults__.items():
        if key not in config:
            config.update({key: default_value})
    
    return config
    
