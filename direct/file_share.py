from tools.html import Parser, Parser_help
from tools.http import Request, HEADER_DEFAULT


class File:
    def __init__(self, url):
        self.url = url

    def oneupload_result(self):
        htt = Request(self.url).rget(headers=HEADER_DEFAULT).text
        pp = Parser(htt).get_bs4()
        data = Parser_help.extract_form_data(pp)
        result = Request(self.url).rpost(data=data, headers=HEADER_DEFAULT, stream=True).url
        return result

    def mediafire_result(self):
        htt = Request(self.url).rget(single=True).text
        pp = Parser(htt).get_bs4()
        return pp.find("a", {"aria-label": "Download file"}).get("href")

    def krakenfiles_result(self):
        htt = Request(self.url).rget(http2=True).text
        Parser(htt).get_bs4()
