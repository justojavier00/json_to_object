import json
import os

def consistent_class_name(data):
    if isinstance(data, dict):
        return f"C{id(data)}"
    elif isinstance(data, list):
        if len(data) == 0:
            return "List"
        elif len(data) == 1:
            return "List[" + consistent_class_name(data[0]) + "]"
        else:
            return "List[Union[" + ", ".join([consistent_class_name(d) for d in data]) + "]]"
    else:
        return type(data).__name__

def generate_python_class(data):
    """
    Generate a single class from a dictionary of data
    and a name for the class.
    """
    data_ = {}
    for key, val in data.items():
        data_[key] = consistent_class_name(val)
    
    # Create the class definition code
    class_def = "@dataclass\nclass " + consistent_class_name(data) + ":\n"
    for key, val in data_.items():
        class_def += "    " + key + ": " + val + "\n"
    
    return class_def

def generate_python_classes(data):
    """
    Generate a class definition for each object in the JSON string.
    """
    class_defs = """
from dataclasses import dataclass
from typing import List, Union

"""
    stack = [data]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            class_def = generate_python_class(value)
            class_defs += class_def + "\n"
            stack.extend(list(value.values()))
        elif isinstance(value, list):
            stack.extend(value)
    return class_defs

def generate_python_file(json_file_path, output_file_path=None):
    output_file_path = output_file_path or os.path.splitext(json_file_path)[0] + ".py"
    with open(json_file_path) as f:
        json_string = f.read()
    class_defs = generate_python_classes(json.loads(json_string))
    with open(output_file_path, "w") as f:
        f.write(class_defs)

