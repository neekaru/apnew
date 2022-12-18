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
    
def starter(url, is_cf: bool = False, single: bool = False):
    """This is for making the website belive we actually visit the site

    Args:
        url (str): the site
        is_cf (bool, optional): This for if the site actually have cloudflare protection. Defaults to False.
        single (bool, optional): This for intend for single requests of site not session. Defaults to False.

    Returns:
        str: The result is different can be status or result
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

def rpost(url: str, is_cf: bool = False, single: bool = False, *args, **kwargs):
    """
    Function Get
    :param is_cf: set True if you scrape cf page
    :param url: input your url to post
    :param single: This for intend for single requests of site not session
    :return: a request
    """
    if is_cf:
        reqcf = cf()
        return reqcf.post(url, *args, **kwargs)
    
    if single:
        return requests.post(url, *args, **kwargs)
    
    return req.post(url, *args, **kwargs)

def rget(url: str, is_cf: bool = False, single: bool = False, *args, **kwargs):
    """
    Function Post
    :param is_cf: set True if you want scrape cf page
    :param url: input your url to get
    :param single: This for intend for single requests of site not session
    """
    if is_cf:
        reqcf = cf()
        return reqcf.get(url, *args, **kwargs)
    
    if single:
        return requests.get(url, *args, **kwargs)

    return req.get(url, *args, **kwargs)
