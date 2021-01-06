from lib.schema.utils import DataType, cat_prefix, call_temp, parse_title


def render_props(title, data: DataType):
    yield from _render_props(None, title, data)


def _render_props(prefix, title, data):
    title_op, title = parse_title(title)
    new_prefix = cat_prefix(prefix, title)
    if isinstance(data, dict):
        for k, v in data.items():
            yield from _render_props(new_prefix, k, v)
    elif isinstance(data, list):
        data_type, args = data
        page = f"Property:{new_prefix}"
        if 'prop_temp' in args:
            content = call_temp(args['prop_temp'])
            yield page, content
        elif 'prop_type' in args:
            content = f"[[具有类型::{args['prop_type']}]]"
            if 'prop_values' in args:
                for t in args['prop_values']:
                    content += f"\n* [[允许取值::{t}]]"
            yield page, content
