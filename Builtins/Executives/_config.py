""" Builtins/Executives/_config.py """

import Modules.exceptions as Exceptions
import Modules.registry as Registry
import Modules.display as Display
import Modules.config as Config


def get_value(args):
    """ Get and display value of 'key' from configuraiton. """
    key = args['key']

    if not key in Registry.__defaults__:
        raise Exceptions.NotFound

    value = Registry.get_value(key)
    print(f'"{key}" = "{value}"')

def set_value(args):
    """ Change value of given key in config."""
    key, new_value = args['key'], args['new_value']

    if not key in Registry.__defaults__:
        raise Exceptions.NotFound

    if new_value == ".":
        Display.Message.info("Setting default value for key as \".\" was used as value.")
        new_value = Registry.__defaults__[key]

    old_value = Registry.get_value(key)
    Registry.set_value(key, new_value)
    Display.Message.success(f'Changed value. ["{old_value}" -> "{new_value}"]')

def show_configuration(_):
    """ Display all settings and it's values. """
    parts = []

    for key, value in Config.get_config().items():
        parts.append(f'"{key}" = "{value}"')

    Display.Message.bullet_list("configuration", parts)
