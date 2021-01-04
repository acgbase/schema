import unittest

import datetime

from lib.wiki import SUploader
from getpass import getpass


class MyTestCase(unittest.TestCase):
    def test_something(self):
        username = 'ACGBaseBot'
        password = getpass("Password:")
        uploader = SUploader(username, password)
        text = "Updated at:" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uploader.upload(f'User:{username}/Sandbox', text)

if __name__ == '__main__':
    unittest.main()
