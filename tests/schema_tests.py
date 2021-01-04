import unittest

from lib.schema import load_schema, render_form, render_template


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
