from Modules.commands import Command, Parameter, EndlessParameter
from Modules.data_types import DataType

import Builtins.Executives._help as exe

Command("stx", exe.syntax_of_command, [Parameter("command_name", DataType.Text, "Which command's syntax will be displayed.")], "Show command's syntax.")
Command("dsc", exe.describe_command, [Parameter("command_name", DataType.Text, "What command will be described")], "Describe command and it's parameters.")
Command("help", exe.show_list, [], "Show list of commands with it's description.")
