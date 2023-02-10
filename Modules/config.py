"""
Module: config.py
Contains default config and user config getter.
"""

import Modules.registry as Registry
import Modules.display as Display

__defaults__ = {
    "prompt": "#gray[#white%cwd#gray] #blue#bold~ #reset",
    "osprefix": ".",
    "defaultdir": "."
}

def get_config() -> dict:
    config = {}

    for key in __defaults__:
        value = Registry.get_value(key) 

        if not value:
            Display.Message.error(f"Cannot get value of key: \"{key}\"")
            value = __defaults__[key]

        config.update({key: value})
    
    return config
