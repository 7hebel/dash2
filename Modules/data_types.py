"""
Module: data_types.py
Custom data types used in parameters reffering to default data types.
"""

class DataType:
    """ Custom data types. """

    def from_string(string: str):
        dictionary = {
            'text': DataType.Text,
            'number': DataType.Number,
            'boolean': DataType.Boolean
        }

        string = string.lower().strip()

        if not string in dictionary:
            return False

        return dictionary[string]


    class Text: 
        """ Normal text (string). """
        name = "Text"
        def __new__(_, value: str) -> str: return str(value)
        @staticmethod
        def validate(value) -> bool: return type(value) == str

    class Number:
        """ Normal number treated as float. """
        name = "Number"
        def __new__(_, value: str) -> float | int:
            if float(value).is_integer(): return int(value)
            else: return float(value)
        @staticmethod
        def validate(value) -> bool: return type(value) in (float, int)

    class Boolean:
        """ Boolean converted from string into True/False form. """
        name = "Boolean"
        def __new__(_, value: str) -> bool:
            if value is True: return True
            if value is False: return False
            if value.strip().lower() in ['1', 'ok', 'true', 't', 'yes', 'y']: return True
            if value.strip().lower() in ['0', 'false', 'f', 'no', 'n']: return False
            raise ValueError
        @staticmethod
        def validate(value) -> bool: return type(value) == bool
