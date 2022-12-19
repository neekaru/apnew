import cloudscraper
import requests
from util.utils import uegen

req = requests.session()

HEADER_DEFAULT: dict = {
        "User-Agent": uegen(default=True),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.6',
        'Sec-Fetch-Mode': 'navigate'
}


def cf():
    """
    just wannabe cf
    """
    reqcq = cloudscraper.create_scraper(browser={
        "browser": "chrome",
        "platform": "windows",
        'mobile': False
    })
    reqcq.headers.update({
        "User-Agent": uegen(default=True),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.6',
        'Sec-Fetch-Mode': 'navigate',
    })
    return reqcq
    
def starter(url, *, is_cf=False, single=False):
    """
    Makes a request to a website and disguises it as a visit by a real user.

    Args:
        url (str): The URL of the website.
        is_cf (bool, optional): Indicates whether the website has Cloudflare protection. Defaults to False.
        single (bool, optional): Makes a single request to the website without maintaining a session. Defaults to False.

    Returns:
        str: The result of the request. This could be the status code or the response content.
    """
    if is_cf:
        reqcf = cf()
        return reqcf.get(url)
    
    headers = {
        "User-Agent": uegen(default=True),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.6',
        'Sec-Fetch-Mode': 'navigate',
    }
    
    if single:
        return requests.get(url, headers=headers)
    
    return req.get(url, headers=headers)


def rpost(url: str, is_cf: bool = False, single: bool = False, *args, **kwargs) -> requests.Response:
    """
    Function Get
    :param url: str: input your url to post
    :param is_cf: bool: set True if you scrape cf page
    :param single: bool: This is intended for single requests of a site, not a session
    :return: requests.Response: a request
    """
    if is_cf:
        reqcf = cf()
        return reqcf.post(url, *args, **kwargs)
    
    if single:
        return requests.post(url, *args, **kwargs)
    
    return req.post(url, *args, **kwargs)

def rget(url: str, is_cf: bool = False, single: bool = False, *args, **kwargs) -> requests.Response:
    """
    Function Get
    :param url: str: input your url to get
    :param is_cf: bool: set True if you want to scrape cf page
    :param single: bool: This is intended for single requests of a site, not a session
    :return: requests.Response: a request
    """

    if is_cf:
        reqcf = cf()
        return reqcf.get(url, *args, **kwargs)
    
    if single:
        return requests.get(url, *args, **kwargs)

    return req.get(url, *args, **kwargs)
