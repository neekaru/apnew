from typing import Tuple, Union

from util.html.parser import fix_url

#  still in beta since i want grab some cookie

class Cookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def clean(self) -> str:
        return self.cookie.split(";")[0]

    def quote(self) -> str:
        return fix_url(self.cookie, quote_plus=True)

    def unquote(self) -> str:
        return fix_url(self.cookie, unquote=True)

class Request:
    def __init__(self, headers):
        self.headers = headers

    def get_cookie(self, *, debug: bool = False, two: bool = False, match: int = None, match1: int = None) -> Union[str, Tuple[str, str]]:
        if two:
            pas1 = self.headers["Set-Cookie"].split(" ")[match]
            pas2 = self.headers["Set-Cookie"].split(" ")[match1]
            return pas1, pas2
        if debug:
            return self.headers["Set-Cookie"].split(" ")
        else:
            pas = self.headers["Set-Cookie"].split(" ")[match]
        return pas

