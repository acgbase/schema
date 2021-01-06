import unittest

from lib.schema.form import render_form
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


if __name__ == '__main__':
    unittest.main()
