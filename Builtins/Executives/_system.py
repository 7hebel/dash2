from datetime import datetime
import random
import sys

import Modules.exceptions as Exceptions
import Modules.display as Display
import Modules.version as Version


def clear_screen(args):
    """ Clear terminal's screen. """
    Display.cls()

def exit_program(args):
    """ Exit dash and reset colors. """
    Display.cls()
    Display.reset_color()
    exit()

def date(args):
    """ Display current date. """
    current_date = datetime.today().strftime("%d/%m/%Y")
    print(f"date: {current_date}")

def time(args):
    """ Display current time. """
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"time: {current_time}")

def say(args):
    """ Display custom content. """
    print(" ".join(args['content']))

def random_number(args):
    """ Generate pseudo random number in given range. """
    lowest = args['lowest']
    highest = args['highest']

    if lowest > highest:
        Display.Message.error(f"lowest greater than highest")
        return

    number = random.randint(lowest, highest)
    print(number)

def check_update(args, session):
    """ Check newest version and compare it with local ver. """
    current = session.version
    online = Version.get_online_version()
    if online.as_text == "0.0.0":
        Display.Message.error("Cannot fetch online version.")
        return

    if current > online or current == online:
        Display.Message.success("You are up to date.")
    if current < online:
        Display.Message.warning(f"Update available: [{current.as_text}] -> [{online.as_text}]")

def update_dash(args, session):
    run_after = args['run_after']
    if run_after is None:
        run_after = True

    current_version = session.version
    online_version = Version.get_online_version()
    if online_version.as_text == "0.0.0":
        Display.Message.error("Cannot fetch online version.")
        return

    if current_version < online_version:
        Display.Message.info(f"[{current_version.as_text}] -> [{online_version.as_text}]")

        try:
            import updater
        except ImportError:
            Display.Message.error("Updater not found.")
            return
        
        updater.make_update(current_version.as_text, run_after)
        sys.exit(0)
