"""
Module: display.py
Contains all funcitons affecting terminal screen.
"""
from colorama import Fore, Style
import platform
import getpass
import ctypes
import sys
import os


def add_color(text) -> str:
    """ Replace style text's (e.g #blue) with actuals styles. """
    formats = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "purple": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "gray": Fore.LIGHTBLACK_EX,
        "reset": Fore.RESET + Style.RESET_ALL,

        "bold": "\033[1m",
        "faint": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "inverted": "\033[7m",
        "crossed": "\033[9m",
    }

    # Replace options with styles / colors.
    for option in formats.keys():
        text = text.replace(f"#{option}", formats[option])

    # Reset at the end.
    text += Style.RESET_ALL

    return text

def cls():
    """ Clear entire screen. """
    os.system("cls || clear")

def clear_last_line():
    """ Clear last line and move cursor to it's beginning. """
    print("\033[1A\033[2K\033[1A")

def reset_color():
    """ Reset current terminal color. """
    print("\033[0;37m", end='')

def init_colors() -> None:
    """ Change console mode to be able to display colors properly. """

    if not sys.stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        if platform.system() == "Windows":
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32

def generate_prompt(session) -> str:
    """ Create displayable form of prompt with colors and vars."""

    def is_admin():
        try:
            is_admin = (os.getuid() == 0)
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return is_admin

    formats = {
        "%cwd": str(session.cwd.absolute().resolve()), # current working directory
        "%drv": session.cwd.drive, # drive name
        "%usr": getpass.getuser(), # system username
        "%mod": "$" if is_admin() else "@" # Shows character based on permissions. 
    }


    # Set prompt text.
    prompt = session.raw_prompt
    for option in formats.keys():
        prompt = prompt.replace(option, formats[option])

    # Format prompt's style.
    prompt = add_color(prompt)
    
    return prompt

class Message:
    """ Formatted messages. """

    def unexpected_error(message: str):
        """ Display unexpected error with red and black colored error prefix and given content. """
        print(f"[\033[7;37;41m UNEXPECTED ERROR \033[0;0;0m] \033[31m{message.capitalize()}\033[0;0m")

    def error(message: str):
        """ Display error with red colored error prefix and given content. """
        print(f"[\033[7;31m ERROR \033[0;0m] \033[31m{message.capitalize()}\033[0;0m")

    def warning(message: str):
        """ Display warning with orange colored warning prefix and given content. """
        print(f"[\033[7;33m WARNING \033[0;0m] \033[33m{message.capitalize()}\033[0;0m")

    def info(message: str):
        """ Display info with blue colored info prefix and given content. """
        print(f"[\033[7;34m INFO \033[0;0m] \033[34m{message.capitalize()}\033[0;0m")
    def success(message: str):
        """ Display success message with green colored success prefix and given content. """
        print(f"[\033[7;32m SUCCESS \033[0;0m] \033[32m{message.capitalize()}\033[0;0m")

    def custom(title: str, message: str):
        """ Display styled message with custom title. """
        print(f"[\033[7;35m {title} \033[0;0m] \033[35m{message.capitalize()}\033[0;0m")

    def bullet_list(title: str, points: list):
        """ Show bullet list with given title and all points. """
        print(f"\n{title.upper()}:")
        for point in points:
            print(f"  \033[1;33m*\033[0;37m {point.strip()}")

        if len(points) == 0:
            print(f"  \033[2;31m(blank list)\033[0;37m")
