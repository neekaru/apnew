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

    def get_cookie(
        self,
        *,
        debug: bool = False,
        val: str = "Set-Cookie",
        two: bool = False,
        match: int = None,
        match1: int = None
    ) -> str | tuple[str, str]:
        if two:
            pas1 = self.headers[val].split(" ")[match]
            pas2 = self.headers[val].split(" ")[match1]
            return pas1, pas2
        if debug:
            return self.headers[val].split(" ")
        else:
            pas = self.headers[val].split(" ")[match]
        return pas
