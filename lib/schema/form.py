from lib.schema.utils import load_template, DataType, cat_prefix


def render_form(title, data):
    content = "\n".join(_render_form(title, 0, None, None, data))
    return load_template('form', title=title, content=content)


def _render_form(ns, depth, prefix, title, data: DataType):
    new_prefix = cat_prefix(prefix, title)
    if isinstance(data, dict):
        items, nodes = _sep_item(data.items())
        if title is not None and depth > 0:
            q = '=' * depth
            yield f"{q} {title} {q}"
        if items:
            yield '{| class="formtable"'
            for i, (k, v) in enumerate(items):
                if i:
                    yield '|-'
                yield from _render_form(ns, depth + 1, new_prefix, k, v)
            yield '|}'
        for k, v in nodes:
            yield from _render_form(ns, depth + 1, new_prefix, k, v)
    else:
        if isinstance(data, list):
            data_type, args = data
        else:
            data_type = data
            args = {}
        if data_type == "single" or data_type == "list":
            prop = ns + "/" + new_prefix
            yield f'! {title}:'
            yield '| ' + "{{{field|" + prop + "}}}"
        elif data_type == "file":
            prop = ns + "/" + new_prefix
            yield f'! {title}:'
            yield "| {{{field|" + prop + "|uploadable|values from namespace=File}}}"



def _sep_item(children):
    items = []
    nodes = []
    for k, v in children:
        if isinstance(v, dict):
            nodes.append((k, v))
        else:
            items.append((k, v))
    return items, nodes
