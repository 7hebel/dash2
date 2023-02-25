from Modules.commands import Command, Parameter
from Modules.data_types import DataType

import Builtins.Executives._config as exe

Command('#get', exe.get_value, [Parameter('key', DataType.Text, 'Config key name.')], "Get value of key from configuration.")
Command('#set', exe.set_value, [Parameter('key', DataType.Text, 'Config key name.'), Parameter('new_value', DataType.Text, 'New value for key in config.')], 'Change value of key in configuration.')
Command('#list', exe.show_configuration, [], 'Show all configuration keys and values.')
