import Modules.exceptions as Exceptions
import Modules.variables as Variables
import Modules.display as Display

def show_all_variables(args):
    """ Display all variables and it's values. """
    Variables.show_all_variables()

def load_from_file(args):
    """ Load variables from file. """
    file_path = args['path']
    try:
        Variables.load_from_file(file_path)
    except:
        raise Exceptions.OsError

def dump_to_file(args):
    """ Dump all user's variables to file. """
    file_path = args['path']
    try:
        Variables.dump_to_file(file_path)
    except:
       raise Exceptions.OsError
    
def add_variable(args):
    """ Add new variable. """
    name = args['name']
    value = args['value']
    raw_data_type = args['data_type']
    if raw_data_type is None:
        raw_data_type = "text"
    Variables.Variable(name, raw_data_type, value)

def remove_variable(args):
    """ Delete variable. """
    name = args['name']

    if not name in Variables.Variable.connections:
        raise Exceptions.NotFound

    Variables.Variable.connections.pop(name)
    Display.Message.success(f'Removed variable: "{name}"')

def edit_value(args):
    """ Edit value of variable. """
    name = args['name']
    new_value = args['new_value']

    if not name in Variables.Variable.connections:
        raise Exceptions.NotFound

    variable_object: Variables.Variable = Variables.Variable.connections[name]
    old_value = variable_object.value
    data_type = variable_object.data_type

    try:
        new_value = data_type(new_value)
        variable_object.value = new_value
        Display.Message.success(f"Changed value. [{old_value} -> {new_value}]")
    except:
        raise Exceptions.DataTypeError
