"""
Module: registry.py
Manage system's registry.
"""

import winreg

from Modules.config import __defaults__

class Keys:
    REGISTRY_PATH = r"Software\dash2"

def create_main_key() -> None:
    """ Create main key in system's registry. """
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, Keys.REGISTRY_PATH)

def set_value(key_name: str, new_value: str) -> None:
    """ 
    Set value of an key. 
    
    @key_name (str): Name of key.
    @new_value (str): New value for key.
    """
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, Keys.REGISTRY_PATH)
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, Keys.REGISTRY_PATH, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(registry_key, key_name, 0, winreg.REG_SZ, new_value)
    winreg.CloseKey(registry_key)

def get_value(key_name: str) -> str | bool:
    """ 
    Get and return value key.

    @key_name (str): Name of key.

    >return (str | False): String value of key or False at error.  
    """
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, Keys.REGISTRY_PATH, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(registry_key, key_name)
        winreg.CloseKey(registry_key)
        return value

    except Exception:
        return False

def create(key_name: str, value: str) -> None:
    """ 
    Create new value key with:
    
    @key_name (str): Name of key.
    @value (str): Value of key.
    """
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, Keys.REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)

    with reg_key:
        if '%' in value:
            var_type = winreg.REG_EXPAND_SZ
        else:
            var_type = winreg.REG_SZ
        winreg.SetValueEx(reg_key, key_name, 0, var_type, value)

def delete(key_name: str) -> None:
    """ Delete key with key_name name """
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, Keys.REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
    winreg.DeleteValue(reg_key, key_name)
        
def check_keys():
    """ Check all keys existance and create missing ones with default values. """
    create_main_key()

    for key, value in __defaults__.items():
        if not get_value(key):
            create(key, value)
