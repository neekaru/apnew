import requests
import cloudscraper

req = requests.session()


HEADER_DEFAULT: dict = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-us,en;q=0.6",
    "Sec-Fetch-Mode": "navigate",
}


class req_add():
    def cf():
        """
        Just wannabe cf temporary
        """
        reqcq = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False})
        reqcq.headers.update({"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                              "Accept-Language": "en-us,en;q=0.6",
                              "Sec-Fetch-Mode": "navigate"})
        return reqcq

    def starter(url, *, single: bool = False):
        """
        Makes a request to a website and disguises it as a visit by a real user.
        """
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.6",
            "Sec-Fetch-Mode": "navigate",
        }
        if single:
            return requests.get(url, headers=headers)

        return req.get(url, headers=headers)


class Request():
    def rpost(url: str, single: bool = False, *args, **kwargs):
        """
        Sends a GET request to the specified URL.
        """
        if single:
            return requests.get(url, *args, **kwargs)

        return req.get(url, *args, **kwargs)

    def rget(url: str, single: bool = False, *args, **kwargs):
        """
        Sends a GET request to the specified URL.
        """
        if single:
            return requests.post(url, *args, **kwargs)

        return req.post(url, *args, **kwargs)
