import os

from lib.run import update


def main():
    username = os.environ['WIKI_USERNAME']
    password = os.environ['WIKI_PASSWORD']
    update(username, password)


if __name__ == '__main__':
    main()
