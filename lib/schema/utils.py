from pathlib import Path
from typing import Union

import yaml

template_root = Path(__file__).parent.parent / 'templates'
schema_root = Path(__file__).parent.parent / 'schemas'

DataType = Union[str, dict]

def load_schema(name):
    fp = schema_root / f"{name}.yaml"
    with open(fp) as f:
        data = yaml.load(f)
    return data


def load_template(template, **kwargs):
    with open(template_root / f"{template}.txt") as f:
        s = f.read()
    for k, v in kwargs.items():
        s = s.replace(f"<<<{k}>>>", v)
    return s


def cat_prefix(prefix, title):
    if prefix and title:
        return f"{prefix}/{title}"
    elif title:
        return title
    else:
        return prefix
