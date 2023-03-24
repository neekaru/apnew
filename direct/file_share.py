from tools.html import Parser
from tools.http import Request


class File:
    def __init__(self, url):
        self.url = url

    def mediafire_result(self):
        htt = Request(self.url).rget(single=True).text
        pp = Parser(htt).get_bs4()
        return pp.find("a", {"aria-label": "Download file"}).get("href")

    def krakenfiles_result(self):
        htt = Request(self.url).rget(http2=True).text
        Parser(htt).get_bs4()
