""" 
Module: commands.py
Classes and functions to manage user input and match it with commands.
"""
from dataclasses import dataclass
from types import FunctionType
from typing import Iterable
import re

import Modules.exceptions as Exceptions
from Modules.data_types import DataType
import Modules.display as Display

def parse_input(string: str) -> tuple[str, list] | None:
    """ Split input into (command, args). Args are split by space.
        longer arguments can be surrounded by "" or ''.

        @string (str): Given input.

        >return (tuple[str, list]): (Command[str], Args[list]) or False
        if command is blank.
    """

    rv = []
    for match in re.finditer(r"('([^'\\]*(?:\\.[^'\\]*)*)'"
                                r'|"([^"\\]*(?:\\.[^"\\]*)*)"'
                                r'|\S+)\s*', string, re.S):
        arg = match.group().strip()
        if arg[:1] == arg[-1:] and arg[:1] in '"\'':
            arg = arg[1:-1].encode('ascii', 'backslashreplace').decode()
        try:
            arg = type(string)(arg)
        except UnicodeError:
            pass
        rv.append(arg)

    try:
        command = rv[0]
    except IndexError:
        return (None, None)
    try:
        args = rv[1:]
    except IndexError:
        args = []

    return (command, args)


@dataclass
class Parameter:
    name: str
    data_type: DataType
    description: str = None
    max_lenght: int = 0
    min_lenght: int = 0
    required: bool = True


@dataclass
class EndlessParameter(Parameter):
    pass


class Command:
    connections = {}

    @staticmethod
    def show_commands_list():
        Display.Message.bullet_list(
            "commands list", 
            [f"{name} - {cmd.description}" for name, cmd in Command.connections.items()]
        )

    def __init__(self, name: str, link_func: FunctionType, params: Iterable[ Parameter | EndlessParameter ], description: str = None, _requires_session: bool = False) -> None:
        self.name = name
        self.params = params
        self.link_func = link_func
        self.description = description 
        self.requires_session = _requires_session

        Command.connections.update({name: self})

    def execute(self, args = [], _session=None):
        """ Execute linked function with given arguments. """
        self.validate_command()
        prepared_args = self.prepare_and_validate_args(args)

        if self.requires_session:
            self.link_func(prepared_args, _session)
        else:
            self.link_func(prepared_args)

    def validate_command(self):
        """ Check if command is proper (including parameters.) """

        taken_names = []
        for index, parameter in enumerate(self.params):

            if parameter.name in taken_names:
                raise Exceptions.ParameterNameTaken

            taken_names.append(parameter.name)

            if isinstance(parameter, EndlessParameter):
                if index != len(self.params)-1:
                    raise Exceptions.EndlessParamNotLast

            if not parameter.required:
                if index < len(self.params)-1:
                    if self.params[index+1].required:
                        raise Exceptions.NotRequiredParamFollowedByRequired

    def prepare_and_validate_args(self, args) -> dict:
        """ Validate arguments (lenght, type...) and put them
        into dictionary. {Parameter.name: given_argument} """

        def check_and_convert_parameter(expected, given):

            # Data type.
            try:
                given = expected.data_type(given)
            except ValueError:
                raise Exceptions.DataTypeError
            
            # Length.
            if expected.data_type in [DataType.Text, DataType.Number]:
                if expected.max_lenght > 0:
                    if len(str(given)) > expected.max_lenght:
                        raise Exceptions.LengthError

                if expected.min_lenght > 0:
                    if len(str(given)) < expected.min_lenght:
                        raise Exceptions.LengthError

            return given

        ready_args = {}

        if self.has_endless_param():
            if len(args) < len(self.params) - self.not_required_count():
                raise Exceptions.AmountError

        elif self.not_required_count() > 0:
            if len(args) < len(self.params) - self.not_required_count():
                raise Exceptions.AmountError

            if len(args) > len(self.params):
                raise Exceptions.AmountError

        else:
            if len(self.params) != len(args):
                raise Exceptions.AmountError

        if len(args) < len(self.params):
            for _ in range(len(self.params)-len(args)):
                args.append(None)

        for expected, given in zip(self.params, args):
            if isinstance(expected, EndlessParameter):
                endless_list = args[args.index(given):]
                ready_list = []

                if endless_list[0] is None:
                    ready_args.update({
                        expected.name: None
                    })

                else:
                    for endless_param in endless_list:
                        endless_param = check_and_convert_parameter(expected, endless_param)
                        ready_list.append(endless_param)

                    ready_args.update({
                        expected.name: ready_list
                    })

            elif not expected.required:
                if not given is None:
                    given = check_and_convert_parameter(expected, given)

                ready_args.update({
                    expected.name: given
                })

            else:
                given = check_and_convert_parameter(expected, given)
                ready_args.update({
                    expected.name: given
                })
            
        return ready_args

    def has_endless_param(self) -> bool:
        if len(self.params) < 1: return False
        return isinstance(self.params[-1], EndlessParameter)

    def not_required_count(self) -> int:
        count = 0
        for param in self.params:
            if not param.required:
                count += 1
        return count 

    def display_syntax(self):
        """ Show readable command syntax. """

        syntax = f"  {self.name} "
        
        for param in self.params:
            if param.required:
                syntax += f"<{param.name}:{str(param.data_type.name)}{':(endless)' if isinstance(param, EndlessParameter) else ''}> "
            else:
                syntax += f"[{param.name}:{str(param.data_type.name)}{':(endless)' if isinstance(param, EndlessParameter) else ''}] "

        Display.Message.bullet_list("syntax", [syntax])

    def display_description(self):
        """ Show command and it's parameters description. """

        points = [f"{self.name}: {self.description}", f"params: {self.get_displayable_parameters_amount()}"]
        points.extend([f'| "{param.name}": {param.description}' for param in self.params])

        Display.Message.bullet_list("description", points)

    def get_displayable_parameters_amount(self) -> str:

        if self.not_required_count() == 0:
            parameters_count = f"{len(self.params)}{'+' if self.has_endless_param() else ''}"
        else:
            parameters_count = f"[{len(self.params) - self.not_required_count()}-{len(self.params)}{'+' if self.has_endless_param() else ''}]"

        return parameters_count
        