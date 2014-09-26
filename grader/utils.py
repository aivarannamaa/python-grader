""" An utility module containing utility functions used by the grader module
    and some useful pre-test hooks.
"""
import json
import traceback
import re


def import_module(path, name=None):
    if name is None:
        name = path
    import importlib.machinery
    loader = importlib.machinery.SourceFileLoader(name, path)
    module = loader.load_module(name)
    return module


def is_function(value):
    try:
        return hasattr(value, '__call__')
    except:
        return False


## Function descriptions
def beautifyDescription(description):
    """ Converts docstring of a function to a test description
        by removing excess whitespace and joining the answer on one
        line """
    lines = (line.strip() for line in description.split('\n'))
    return " ".join(filter(lambda x: x, lines))


def setDescription(function, description):
    import grader
    old_description = grader.get_test_name(function)
    if old_description in grader.testcases:
        grader.testcases.remove(old_description)
    description = beautifyDescription(description)
    function.__doc__ = description
    grader.testcases.add(description, function)


## Json managing
def load_json(json_string):
    " Loads json_string into an dict "
    return json.loads(json_string)


def dump_json(ordered_dict):
    " Dumps the dict to a string, indented "
    return json.dumps(ordered_dict, indent=4)

def extract_numbers(s, decimal_comma=True):
    result = []
    if decimal_comma:
        rexp = """((?:\+|\-)?\d+(?:(?:\.|,)\d+)?)"""
    else:
        rexp = """((?:\+|\-)?\d+(?:\.\d+)?)"""
        
    for item in re.findall(rexp, s):
        try:
            result.append(int(item))
        except:
            try:
                result.append(float(item.replace(",", ".")))
            except:
                pass
    return result

def get_error_message(exception):
    type_ = type(exception)
    return "{}: {}".format(type_.__name__, str(exception))


def get_traceback(exception):
    type_, value, tb = type(exception), exception, exception.__traceback__
    return "".join(traceback.format_exception(type_, value, tb))


def read_code(path):
    import tokenize
    # encoding-safe open
    with tokenize.open(path) as sourceFile:
        contents = sourceFile.read()
    return contents
