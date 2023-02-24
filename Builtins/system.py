from Modules.commands import Command, Parameter, EndlessParameter
from Modules.data_types import DataType

import Builtins.Executives._system as exe

Command("exit", exe.exit_program, [], "Exit program.")
Command("date", exe.date, [], "Display current date.")
Command("time", exe.time, [], "Display current time.")
Command("cls", exe.clear_screen, [], "Clear screen.") 
Command("say", exe.say, [EndlessParameter("content", DataType.Text, "Content to display")], "Display custom content on the screen.")
Command("rng", exe.random_number, [Parameter("lowest", DataType.Number, "Lowest number possible."), Parameter("highest", DataType.Number, "Highest number possible.")], "Generate random number in given range.")
Command("ver", exe.check_update, [], "Check if dash is up to date.", True)
Command("update", exe.update_dash, [Parameter("run_after", DataType.Boolean, "Should dash open after update?", required=False)], "Upgrade dash if any update is available.", True)
