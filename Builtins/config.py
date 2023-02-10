from Modules.commands import Command, Parameter, EndlessParameter
from Modules.data_types import DataType

import Builtins.Executives._config as exe

Command('#get', exe.get_config_value, [Parameter('key', DataType.Text, 'Config key name.')], "Get value of key from configuration.")
Command('#set', exe.set_config_value, [Parameter('key', DataType.Text, 'Config key name.'), Parameter('new_value', DataType.Text, 'New value for key in config.')], 'Change value of key in configuration.')
Command('#list', exe.display_configuration, [], 'Show all configuration keys and values.')
