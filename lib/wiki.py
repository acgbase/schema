import hashlib
import time
import traceback
from pathlib import Path

import mwclient
import requests

pagehash = Path(__file__).parent.parent / 'pagehash'


class SUploader:
    def __init__(self, username, password):
        self.site = mwclient.Site('acgbase.huijiwiki.com')
        self.site.login(username, password)
        self._cmp = _FileCmp()

    def upload(self, title, text):
        if self._cmp(title, text):
            print("Upload:", title)
            page = self.site.pages[title]
            self._safe_edit(page, text)
            return True
        else:
            print("Ignore:", title)
            return False

    def _safe_edit(self, page, text):
        while True:
            try:
                page.edit(text=text, summary='schema bot maintaining')
            except (mwclient.errors.APIError, requests.exceptions.RequestException):
                traceback.print_exc()
                time.sleep(20)
            else:
                break


class _FileCmp:
    def __call__(self, name, text):
        old_hash = self._read_page_hash(name)
        new_hash = self._hash_page(text)
        if old_hash == new_hash:
            return False
        else:
            self._write_page_hash(name, new_hash)
            return True

    def _read_page_hash(self, name):
        fp = self._hash_file(name)
        if not fp.exists():
            return None
        with open(fp) as f:
            return f.read()

    def _hash_page(self, text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _write_page_hash(self, name, fhash):
        fp = self._hash_file(name)
        with open(fp, 'w') as f:
            f.write(fhash)

    def _hash_file(self, name):
        name = name.replace(":", "_").replace("/", "_")
        return pagehash / f'{name}.txt'
