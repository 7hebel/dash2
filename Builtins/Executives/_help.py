from Modules.commands import Command
import Modules.display as Display

def syntax_of_command(args):
    """ Display syntax of an command. """
    name = args['command_name']

    if not name in Command.connections:
        Display.Message.error(f"Command: {name} not found.")
        return

    command_object = Command.connections[name]
    command_object.display_syntax()

def describe_command(args):
    """ Show description of command and it's parameters. """
    name = args['command_name']

    if not name in Command.connections:
        Display.Message.error(f"Command: {name} not found.")
        return

    command_object = Command.connections[name]
    command_object.display_description()

def show_list(args):
    """ Show list of all available commands. """
    Command.show_commands_list()
    