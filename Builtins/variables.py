from Modules.commands import Command, Parameter, EndlessParameter
from Modules.data_types import DataType

import Builtins.Executives._variables as exe

Command("$list", exe.show_all_variables, [], "Show all variables, according data types and values.")
Command("$load", exe.load_from_file, [Parameter("path", DataType.Text, "Path to file.")], "Load all variables from file.")
Command("$dump", exe.dump_to_file, [Parameter("path", DataType.Text, "Path to file (does not have to exists).")], "Save all variables to file.")
Command("$add", exe.add_variable, [Parameter("name", DataType.Text, "Name of variable."), Parameter("value", DataType.Text, "Variable's value"), Parameter("data_type", DataType.Text, "Specify data type.", required=False)], "Create new variable.")
Command("$del", exe.remove_variable, [Parameter("name", DataType.Text, "Name of variable.")], "Remove variable.")
Command("$edit", exe.edit_value, [Parameter("name", DataType.Text, "Variable name."), Parameter("new_value", DataType.Text, "New value of variable.")], "Change value of variable.")
