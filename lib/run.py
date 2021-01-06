import os

from lib.schema.form import render_form
from lib.schema.template import render_template
from lib.schema.utils import load_schema
from lib.wiki import SUploader

def get_schemas():
    for s in os.listdir("schemas"):
        n, _ = os.path.splitext(s)
        yield n

def update(username, password):
    uploader = SUploader(username, password)
    for nm in get_schemas():
        data = load_schema(nm)
        form = render_form(nm, data)
        temp = render_template(nm, data)
        uploader.upload(f"Form:{nm}", form)
        uploader.upload(f"Template:{nm}", temp)
