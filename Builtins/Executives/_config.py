import Modules.exceptions as Exceptions
import Modules.registry as Registry
import Modules.display as Display
import Modules.config as Config


def get_config_value(args):
    """ Get and display value of 'key' from configuraiton. """
    key = args['key']

    if not key in Registry.__defaults__:
        raise Exceptions.NotFound

    value = Registry.get_value(key)
    print(f'"{key}" = "{value}"')

def set_config_value(args):
    """ Change value of given key in config."""
    key = args['key']
    new_value = args['new_value']

    if not key in Registry.__defaults__:
        raise Exceptions.NotFound

    if new_value == ".":
        Display.Message.info("Setting default value for key as \".\" was used as value.")
        new_value = Registry.__defaults__[key]

    old_value = Registry.get_value(key)
    Registry.set_value(key, new_value)
    Display.Message.success(f'Changed value. ["{old_value}" -> "{new_value}"]')

def display_configuration(args):
    """ Display all settings and it's values. """
    points = []

    for key, value in Config.get_config().items():
        points.append(f'"{key}" = "{value}"')

    Display.Message.bullet_list("configuration", points)
