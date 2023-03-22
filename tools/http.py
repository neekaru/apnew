import cloudscraper
import httpx
import requests

from tools.uegen import User_Agent

req = requests.session()
req_2 = httpx.Client(http2=True)

HEADER_DEFAULT: dict = {
    "User-agent": User_Agent.GetRandomUserAgent(),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-us,en;q=0.6",
    "Sec-Fetch-Mode": "navigate",
}


class Request:
    def __init__(self, url: str):
        self.url = url

    def rpost(self, single: bool = False, http2: bool = False, *args, **kwargs):
        """
        Sends a POST request to the specified URL.
        """
        if http2:
            return req_2.post(self.url, *args, **kwargs)

        if single:
            return requests.post(self.url, *args, **kwargs)

        return req.post(self.url, *args, **kwargs)

    def rget(self, single: bool = False, http2: bool = False, *args, **kwargs):
        """
        Sends a GET request to the specified URL.
        """
        if http2:
            return req_2.get(self.url, *args, **kwargs)

        if single:
            return requests.get(self.url, *args, **kwargs)

        return req.get(self.url, *args, **kwargs)


class Request_Add:
    def __init__(self, url):
        self.url = url

    def cf(self):
        """
        Just wannabe cf temporary
        """
        reqcq = cloudscraper.create_scraper(
            browser={"browser": "chrome",
                     "platform": "windows", "mobile": False}
        )
        reqcq.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us,en;q=0.6",
                "Sec-Fetch-Mode": "navigate",
            }
        )
        return reqcq

    @staticmethod
    def get_headers(
        additional_headers: dict = None,
        edit_headers: dict = None,
        drop_headers: list = None,
    ):
        headers = HEADER_DEFAULT
        if edit_headers:
            headers.update(edit_headers)
        if drop_headers:
            for header in drop_headers:
                if header in headers:
                    del headers[header]
        if additional_headers:
            headers.update(additional_headers)
        return headers

    def starter(self, *, single: bool = False):
        """
        Makes a request to a website and disguises it as a visit by a real user.
        """
        headers = {
            "User-Agent": User_Agent.GetRandomUserAgent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.6",
            "Sec-Fetch-Mode": "navigate",
        }
        if single:
            return requests.get(self.url, headers=headers)

        return req.get(self.url, headers=headers)
