import unittest

from lib.schema.form import render_form
from lib.schema.prop import render_props
from lib.schema.template import render_template
from lib.schema.utils import load_schema


class MyTestCase(unittest.TestCase):
    def test_form(self):
        s = load_schema("人物信息")
        print(s)
        res = render_form("人物信息", s)
        print(res)

    def test_template(self):
        s = load_schema("人物信息")
        print(s)
        res = render_template("人物信息", s)
        print(res)

    def test_prop(self):
        s = load_schema("人物信息")
        print(s)
        for k, v in render_props("人物信息", s):
            print(f"=========== {k} ===========")
            print(v)
            print()


if __name__ == '__main__':
    unittest.main()
