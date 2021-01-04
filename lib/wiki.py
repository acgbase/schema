import mwclient


class SUploader:
    def __init__(self, username, password):
        self.site = mwclient.Site('acgbase.huijiwiki.com')
        self.site.login(username, password)

    def upload(self, title, text):
        page = self.site.pages[title]
        page.edit(text=text, summary='schema bot maintaining')
