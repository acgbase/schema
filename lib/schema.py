import json
from pathlib import Path
from typing import Union
import yaml

DataType = Union[str, dict]

template_root = Path(__file__).parent.parent / 'templates'
schema_root = Path(__file__).parent.parent / 'schemas'


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


def render_form(title, data):
    content = "\n".join(_render_form(0, None, None, data))
    return load_template('form', title=title, content=content)


def _render_form(depth, prefix, title, data: DataType):
    new_prefix = _cat_prefix(prefix, title)
    if data == "single" or data == "list":
        yield f'! {title}:'
        yield '| ' + "{{{field|" + new_prefix + "}}}"
    else:
        items, nodes = _sep_item(data.items())
        if title is not None:
            q = '=' * depth
            yield f"{q} {title} {q}"
        if items:
            yield '{| class="formtable"'
            for i, (k, v) in enumerate(items):
                if i:
                    yield '|-'
                yield from _render_form(depth + 1, new_prefix, k, v)
            yield '|}'
        for k, v in nodes:
            yield from _render_form(depth + 1, new_prefix, k, v)


def _sep_item(children):
    items = []
    nodes = []
    for k, v in children:
        if isinstance(v, dict):
            nodes.append((k, v))
        else:
            items.append((k, v))
    return items, nodes


def _cat_prefix(prefix, title):
    if prefix and title:
        return f"{prefix}/{title}"
    elif title:
        return title
    else:
        return prefix


def render_template(title, data):
    keys = get_all_keys(data)
    help = _render_template_help_msg(keys)
    meta = _render_template_meta(keys)
    content = "\n".join(_render_template(None, None, data))
    return load_template('template', title=title, help=help, meta=meta, content=content)


def _render_template(prefix, title, data):
    new_prefix = _cat_prefix(prefix, title)
    if data == 'single':
        yield f"* '''{new_prefix}:''' [[{new_prefix}::" + "{{{" + new_prefix + "| {{auto|single|" + new_prefix + "}} }}}]]"
    elif data == 'list':
        yield f"* '''{new_prefix}:'''"+"{{#arraymap:{{{" + new_prefix + "| {{auto|list|" + new_prefix + "}} }}}|,|x|[[" +new_prefix + "::x]]}}"
    else:
        if title:
            yield "{{Form/Box|" + title + "|"
        else:
            yield "{{Form/Box| |"
        for k, v in data.items():
            yield from _render_template(new_prefix, k, v)
        yield "}}"


def get_all_keys(data):
    return list(_get_prefixes(None, data))


def _get_prefixes(prefix, data):
    if isinstance(data, dict):
        for k, v in data.items():
            yield from _get_prefixes(_cat_prefix(prefix, k), v)
    else:
        yield prefix


def _render_template_help_msg(keys):
    return "\n".join(f"|{k}=" for k in keys)


def _render_template_meta(keys):
    data = {
        'params': {
            k: {"suggested": True}
            for k in keys
        }
    }
    return json.dumps(data, ensure_ascii=False)
