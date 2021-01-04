import json
import os

from lib.schema import render_form, load_schema, render_template
from lib.wiki import SUploader

def get_schemas():
    for s in os.listdir("schemas"):
        n, _ = os.path.splitext(s)
        yield n


def main():
    auth = json.load(open('auth.local.json'))
    username = auth['username']
    password = auth['password']
    uploader = SUploader(username, password)
    for nm in get_schemas():
        data = load_schema(nm)
        form = render_form(nm, data)
        temp = render_template(nm, data)
        uploader.upload(f"Form:{nm}", form)
        uploader.upload(f"Template:{nm}", temp)


if __name__ == '__main__':
    main()
