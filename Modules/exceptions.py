"""
Module: exceptions.py
Contains custom errors.
"""
from Modules.display import Message  

def handle_error(exception: Exception):
    try:
        exception.__module__
        Message.error(str(exception))

    except AttributeError:
        Message.unexpected_error(str(exception))

class NotFound(Exception):
    def __str__(self) -> str: return "Not found."
class AmountError(Exception):
    def __str__(self) -> str: return "Invalid amount of parameters. (check command's description.)"
class DataTypeError(Exception):
    def __str__(self) -> str: return "Invalid data type."
class LengthError(Exception): 
    def __str__(self) -> str: return "Invalid parameter length."

class ParameterNameTaken(Exception):
    def __str__(self) -> str: return "Parameter name already taken."
class EndlessParamNotLast(Exception): 
    def __str__(self) -> str: return "Endless parameter is found not as last."
class NotRequiredParamFollowedByRequired(Exception): 
    def __str__(self) -> str: return "Not required parameter followed by an required one."

class NameAlreadyTaken(Exception):
    def __str__(self) -> str: return "This name is already taken."
class NoPermissions(Exception): 
    def __str__(self) -> str: return "No required permissions to proceed."
class OsError(Exception): 
    def __str__(self) -> str: return "Something went wrong with system."
class NotDirectory(Exception):
    def __str__(self) -> str: return "This is not a directory."
class NotExists(Exception): 
    def __str__(self) -> str: return "This object does not exists."

class CannotGatherInfo(Exception): 
    def __str__(self) -> str: return "Cannot gather information."
class InvalidAddress(Exception): 
    def __str__(self) -> str: return "Invalid address."
