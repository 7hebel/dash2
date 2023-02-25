__version__ = "1.1.0"

import os

import Modules.exceptions as Exceptions
import Modules.data_types as DataTypes
import Modules.variables as Variables
import Modules.registry as Registry
import Modules.commands as Commands 
import Modules.display as Display
import Modules.version as Version
import Modules.session as Session
import Modules.config as Config
import Builtins.ALL
import updater

Registry.check_keys()
Display.init_colors()
Display.cls()

# Main session.
session = Session.Session()

# Version control.
version = Version.get_version_from_text(__version__)
online_version = Version.get_online_version()
session.version = version

if online_version > version:
    Display.Message.warning(f"Newer version detected: [{version.as_text} -> {online_version.as_text}]")

    if session.auto_update:
        Display.Message.info("autoupdate is enabled, updating...")
        updater.make_update()

if online_version.as_tuple == (0, 0, 0):
    Display.Message.error(f"Failed to detect online version.")

# Sytem variables.
Variables.Variable("ver", DataTypes.DataType.Text, version, True)

# Auto load Varsdump.
if session.varsdump != False:
    Variables.load_from_file(session.varsdump)
    

while 1:
    session.refresh_config()
    
    try:
        user_input = input("\n"+Display.generate_prompt(session))
        user_input = Variables.replace_names_with_values(user_input)

    except KeyboardInterrupt:
        Commands.Command.connections['exit'].execute()

    # System command.
    if user_input.startswith(session.osprefix):
        Display.Message.info("(using system shell)\n")
        os.system(user_input.replace(session.osprefix, '', 1))
        continue

    command_name, args = Commands.parse_input(user_input)

    if command_name is None: continue
    if not command_name in Commands.Command.connections:
        Display.Message.error(f"Command not found: \"{command_name}\"")
        continue

    command_object: Commands.Command = Commands.Command.connections[command_name]

    try:
        command_object.execute(args, session)

    except Exception as exception:
        Exceptions.handle_error(exception)
