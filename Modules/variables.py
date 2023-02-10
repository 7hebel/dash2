from typing import Any
import json
import os

from Modules.data_types import DataType
import Modules.display as Display


class Variable:
    connections = {}
    system_connections = {}

    def __init__(self, name: str, _data_type: str | DataType, value: Any, is_system=False) -> None:
        self.name: str = name
        if self.name.strip() == "":
            Display.Message.error(f'Cannot parse variable (blank name)')
            del self
            return
        if self.name in Variable.connections:
            Display.Message.error(f'Variable name: "{name}" already taken.')
            del self
            return
        if '$' in self.name:
            Display.Message.error(f'Invalid character: "$" in name.')
            del self
            return
        self.data_type = _data_type
        if isinstance(_data_type, str):
            self.data_type = DataType.from_string(_data_type)
        if not self.data_type:
            Display.Message.error(f'Cannot parse variable: "{name}" (invalid data type: "{_data_type}")')
            del self
            return
        self.value = value
        try:
            self.convert_self_value()
        except:
            Display.Message.error(f'Cannot parse variable: "{name}" (invalid value for data type)')
            del self
            return
        if self.name in Variable.connections.items():
            Display.Message.error(f'Variable name: "{self.name}" already taken.')
            del self
            return
        self.is_system = is_system

        if not self.is_system:
            Variable.connections.update({self.name: self})
        else:
            Variable.system_connections.update({self.name: self})

    def convert_self_value(self):
        self.value = self.data_type(self.value)


# In file content: {'name': {'value': ..., 'data_type': text/number/boolean}}

def load_from_file(file_path: str):

    failed = 0
    success = 0

    if not os.path.exists(file_path):
        Display.Message.error(f'File: "{file_path}" does not exists.')
        return

    with open(file_path, "r", encoding="utf8") as file_obj:
        content = json.load(file_obj)

    if content == {}:
        Display.Message.error(f'No variables in file.')
        return

    for name, content in content.items():
        
        if 'value' not in content:
            Display.Message.error(f'Cannot parse variable: "{name}" (no "value" entry)')
            failed += 1
            continue

        if 'data_type' not in content:
            Display.Message.error(f'Cannot parse variable: "{name}" (no "data_type" entry)')
            failed += 1
            continue
        
        value = content['value']
        raw_data_type = content['data_type']
        data_type = DataType.from_string(raw_data_type)

        if value == "":
            Display.Message.error(f'Cannot parse variable: "{name}" (blank value)')
            failed += 1
            continue

        if not data_type:
            Display.Message.error(f'Cannot parse variable: "{name}" (invalid value for data type)')
            failed += 1
            continue

        if '$' in name:
            Display.Message.error(f'Invalid character: "$" in name.')
            failed += 1 
            continue
        
        Variable(name, data_type, value)
        success += 1 

    if success > 1 and failed == 0:
        Display.Message.success(f'All {success} variables from: "{file_path}" loaded successfully.')
        
    if success > 1 and failed > 1:
        Display.Message.warning(f'Loaded {success} variables, {failed} failed.')

    if success == 0 and failed > 1:
        Display.Message.error(f'No variables loaded, {failed} failed.')

def dump_to_file(file_path: str):
    content = {}
    count = 0

    if Variable.connections == {}:
        Display.Message.error("No variables are set.")
        return

    if not os.path.exists(file_path):
        open(file_path, 'a+', encoding='utf-8').close()
        Display.Message.info("Created dump file.")

    for name, variable in Variable.connections.items():
        content.update({
            name: {
                'value': variable.value,
                'data_type': variable.data_type.name
            }
        })
        count += 1

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(content, file)

    Display.Message.success(f'Saved {count} variables to "{file_path}".')

def replace_names_with_values(text: str) -> str:
    for name, variable in Variable.system_connections.items():
        text = text.replace(f"$${name}$$", str(variable.value))

    for name, variable in Variable.connections.items():
        text = text.replace(f"${name}$", str(variable.value))

    return text

def show_all_variables():
    Display.Message.bullet_list(
        "user variables", 
        [f'"{name}" = ({variable.data_type.name}) "{variable.value}"' for name, variable in Variable.connections.items()]    
    )

    Display.Message.bullet_list(
        "system variables", 
        [f'"{name}" = ({variable.data_type.name}) "{variable.value}"' for name, variable in Variable.system_connections.items()]    
    )
      
