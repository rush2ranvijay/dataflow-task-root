"""
General Purpose utilities
"""
import importlib
import math
import uuid
from typing import Tuple

import pandas as pd
from dateutil import parser
from flatten_json import flatten
from tabulate import tabulate

from task_ops.exceptions import IllegalArgumentException

_BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'True': True, 'on': True, 'Yes': True, 'Y': True, 'y': True,
                   '0': False, 'no': False, 'false': False, 'False': False, 'off': False, 'No': False,
                   'N': False, 'n': False, 'None': False, 'none': False, 'null': False}


def flag(value: any) -> bool:
    return _BOOLEAN_STATES[value] if value in _BOOLEAN_STATES else bool(value)


def flatten_dict(data: dict) -> dict:
    return flatten(data, separator='.')


def module_and_class_name(fqn: str) -> Tuple:
    last_dot = fqn.rfind(".")
    if last_dot == -1 or fqn[-1] == '.':
        raise IllegalArgumentException(f"must be an fully qualified name of class. But it was: {fqn}")
    return fqn[0:last_dot], fqn[last_dot + 1:]


def instantiate(fqn: str, class_kwargs: dict):
    module_name, class_name = module_and_class_name(fqn)
    try:
        if class_kwargs is None:
            class_kwargs = {}
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        return class_(**class_kwargs)
    except (ImportError, AttributeError) as e:
        raise IllegalArgumentException(f"no class available with given name: {fqn} - {str(e)}")


def required_not_none(config: dict, key: str, message: str):
    if key not in config:
        raise IllegalArgumentException(message)
    return required_param(config[key], message)


def required_param(value: str, message: str):
    if not value:
        raise IllegalArgumentException(message)
    return value


def parse_charset_from_content_type(content_type: str, fallback: str = None):
    if not content_type:
        return fallback
    tokens = content_type.split(';')
    content_type, params = tokens[0].strip(), tokens[1:]
    params_dict = {}
    items_to_strip = "\"' "

    for param in params:
        param = param.strip()
        if param:
            key, value = param, True
            index_of_equals = param.find("=")
            if index_of_equals != -1:
                key = param[:index_of_equals].strip(items_to_strip)
                value = param[index_of_equals + 1:].strip(items_to_strip)
            params_dict[key.lower()] = value

    return params_dict.get('charset', fallback)


def remove_entry_if_none(data: dict, key: str):
    if key in data and not data[key]:
        data.pop(key)


def get_uuid():
    return str(uuid.uuid4())


def parse_date(dt_str):
    return parser.parse(dt_str).date()


def un_flatten(d: dict):
    result = dict()
    for key, value in d.items():
        parts = key.split(".")
        d = result
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return result


def make_ascii_table(df: pd.DataFrame):
    return tabulate(df, df.columns, showindex=False, tablefmt="fancy_grid")


def get_quarter_year(d):
    return math.ceil(d.month / 3), d.year
