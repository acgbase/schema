import json

from lib.schema.utils import load_template, cat_prefix


def render_template(title, data):
    keys = [f"{title}/{k}" for k in get_all_keys(data)]
    help = _render_template_help_msg(keys)
    meta = _render_template_meta(keys)
    content = "\n".join(_render_template(title, None, None, data))
    return load_template('template', title=title, help=help, meta=meta, content=content)


def _render_template(ns, prefix, title, data):
    new_prefix = cat_prefix(prefix, title)
    if isinstance(data, dict):
        if title:
            yield "{{Form/Box|" + title + "|"
        else:
            yield "{{Form/Box|" + ns + "|"
        for k, v in data.items():
            yield from _render_template(ns, new_prefix, k, v)
        yield "}}"
    else:
        if isinstance(data, list):
            data_type, args = data
        else:
            data_type = data
            args = {}
        prop = ns + '/' + new_prefix
        val_temp = None
        if 'display' in args:
            val_temp = _template_display_temp[args['display']]
        if data_type == 'single':
            value_getter = "{{{" + prop + "| {{auto|single|" + prop + "}} }}}"
            content = _template_render_value(prop, value_getter, val_temp)
        elif data_type == 'list':
            value_getter = "{{{" + prop + "| {{auto|list|" + prop + "}} }}}"
            _renderer = _template_render_value(prop, "x", val_temp)
            content = _call_special_temp("arraymap", value_getter, ",", "x", _renderer)
        elif data_type == 'file':
            value_getter = "{{{" + prop + "| {{auto|single|" + prop + "}} }}}"
            content = "[[File:" + value_getter + "|300px|link=]] {{#set:" + prop + " = " + value_getter + " }}"
        else:
            raise ValueError(data)
        yield _call_temp("Form/Box/Item", title, content)

def _template_render_value(prop, val_sym, val_temp):
    if val_temp is None:
        return f"[[{prop}::{val_sym}]]"
    else:
        return f"[[{prop}::{val_sym}]]" + _call_temp(val_temp, val_sym)

def _call_temp(name, *args):
    return "{{" + name + "|" + "|".join(args) + "}}"

def _call_special_temp(name, *args):
    return "{{#" + name + ":" + "|".join(args) + "}}"

_template_display_temp = {
    'color': '属性/颜色'
}



def get_all_keys(data):
    return list(_get_prefixes(None, data))


def _get_prefixes(prefix, data):
    if isinstance(data, dict):
        for k, v in data.items():
            yield from _get_prefixes(cat_prefix(prefix, k), v)
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
