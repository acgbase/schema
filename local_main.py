import json
import os

from lib.run import update
from lib.wiki import SUploader

def get_schemas():
    for s in os.listdir("schemas"):
        n, _ = os.path.splitext(s)
        yield n


def main():
    auth = json.load(open('auth.local.json'))
    username = auth['username']
    password = auth['password']
    update(username, password)


if __name__ == '__main__':
    main()
