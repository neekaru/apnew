from bs4 import BeautifulSoup
from w3lib.url import url_query_cleaner
import urllib.parse


def get_bs4(url):
    """
    Beautifulbs4 simple function
    :param url: for url
    :return: beautiful function
    """
    return BeautifulSoup(url, "html.parser")

# porting from old api
def getfilehost(url, hostname=False):
    """
    Unused idk since it's no have perpouse
    """
    if hostname is True:
        url = url.strip("/ ")
        return url.split("/")[2]
    else:
        url = url.strip("/ ")
        return url.split("/")[-1]

def cleanurl(url: str, *args, **kwargs):
    return url_query_cleaner(url, *args, **kwargs)

def trailing(bs4, quotation_mark=False, apostrophe=False, combo=False):
    """Trailing Text
    This intended for string with question mark and apostrophe
    also this have a combo argument for something where "'" and '"' is exist

    Args:
        bs4 (str): _description_
        quotation_mark (bool, optional): For removing quotation mark in string. Defaults to False.
        apostrophe (bool, optional): For removing apostrophe in string. Defaults to False.
        combo (bool, optional): For apostrophe and quotation mark where something like ("a":'bbb'). Defaults to False.

    Returns:
        str: result
    """
    if quotation_mark:
        return bs4.replace('"', '')
    if apostrophe:
        return bs4.replace("'", "")
    if combo:
        return bs4.replace("'", "").replace('"', ' ')

def fix_url(url: str, clean=False, quote_plus=False, quote=False, quote_fix=False, unquote=False):
    """ This for helping fix url stuff for quote and unquote

    Args:
        url (str): for fixing stuff like coolrom where they need quote the parameter
        clean (bool, optional): for cleaning some url like this "/\ /". Defaults to False.
        quote_plus (bool, optional): same as above but more complex. Defaults to False.
        quote (bool, optional): for making quote. Defaults to False.
        quote_fix (bool, optional): for fixing stuff like coolrom where, the parameter like the filename need to be quote. Defaults to False.
        unquote (bool, optional): for unquote some url. Defaults to False.

    Returns:
        any: a fixed url
    """
    
    if quote_fix is True:
        return urllib.parse.quote(url, safe="/:")
    elif unquote is True:
        return urllib.parse.unquote(url)
    elif quote_plus is True:
        return urllib.parse.quote_plus(url)
    elif quote is True:
        return urllib.parse.quote(url)
    elif clean is True:
        return url.replace("\\", "")

def get_link_single(bs4, a_style=False, href_style=False):
    """
    Function get_links
    :param a_style: if the url using <a href="">
    :param href_style: if the url format something like this <a class="" href="">
    :result: get url
    """
    if a_style is True:
        return bs4.find("a").get("href")
    elif href_style is True:
        return bs4.get("href")

def get_title(bs4, generic=False, force=False, *args, **kwargs):
    """
    Function Get_title
    :param generic: to be generic using title
    :param force: to forcing to get title
    :result: title 
    """
    if generic is True:
        d = bs4.find("title").get_text()
    elif force is True:
        d = bs4.get_text()
    else:
        d = bs4.find(*args, **kwargs).get_text() 
    return d