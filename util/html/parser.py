import re
import urllib.parse
from typing import Any, Dict, Union

from bs4 import BeautifulSoup
from w3lib.url import url_query_cleaner

from util.network.http import rget, rpost


def get_bs4(url):
    """
    Beautifulbs4 simple function
    :param url: for url
    :return: beautiful function
    """
    return BeautifulSoup(url, "html.parser")

def download_webpage_with_post(url: str, cf: bool = False, single: bool = False, parse_as: str = "html", headers: Dict[str, str] = None, data: Dict[str, Any] = None, *args, **kwargs) -> Union[BeautifulSoup, str, Dict[str, Any]]:
    # sourcery skip: raise-specific-error
    """
    Downloads and optionally parses the response of a webpage using a POST request.
    
    Parameters:
        url (str): The URL of the webpage to download.
        cf (bool): A flag indicating whether to use the cloudscraper on requests.post() function which can handles Cloudflare protection.
        single (bool): A flag if you want use single requests not session
        parse_as (str): A string indicating how to parse the response. Can be "html", "text", or "json".
        headers (Dict[str, str]): A dictionary of HTTP headers to send with the request.
        data (Dict[str, Any]): A dictionary of data to send in the body of the request.
        *args: Additional positional arguments to pass to the requests.post() or cf() function.
        **kwargs: Additional keyword arguments to pass to the requests.post() or cf() function.
        
    Returns:
        BeautifulSoup, str, or Dict[str, Any]: A BeautifulSoup object containing the parsed HTML of the webpage, the raw response text as a string, or the response JSON data as a dictionary, depending on the value of `parse_as`.
        
    Raises:
        Exception: If the request to the webpage fails.
    """
    if cf:
        response = rpost(url, headers=headers, is_cf=True, data=data, *args, **kwargs)
    elif single:
        response = rpost(url, headers=headers, single=True, data=data, *args, **kwargs)
    else:
        response = rpost(url, headers=headers, data=data, *args, **kwargs)

    if response.status_code != 200:
        raise Exception(f'Request to {url} failed with status code {response.status_code}')

    if parse_as == "html":
        return BeautifulSoup(response.text, 'html.parser')
    elif parse_as == "json":
        return response.json()
    elif parse_as == "text":
        return response.text



def download_webpage(url: str, cf: bool = False, single: bool = False, parse_as: str = "html", headers: Dict[str, str] = None, *args, **kwargs) -> Union[BeautifulSoup, str]:
    # sourcery skip: raise-specific-error
    """
    Downloads and parses the HTML of a webpage.
    
    Parameters:
        url (str): The URL of the webpage to download.
        cf (bool): A flag indicating whether to use the cloudscraper on requests.get() function which can handles Cloudflare protection.
        single (bool): A flag if you want use single requests not session
        parse_as (str): A string indicating how to parse the response. Can be "html", "text", or "json".
        headers (Dict[str, str]): A dictionary of HTTP headers to send with the request.
        *args: Additional positional arguments to pass to the requests.get() or cf() function.
        **kwargs: Additional keyword arguments to pass to the requests.get() or cf() function.
        
    Returns:
        BeautifulSoup: A BeautifulSoup object containing the parsed HTML of the webpage.
        
    Raises:
        Exception: If the request to the webpage fails.
    """
    if cf:
        response = rget(url, headers=headers, is_cf=True, *args, **kwargs)
    elif single:
        response = rget(url, headers=headers, single=True, *args, **kwargs)
    else:
        response = rget(url, headers=headers, *args, **kwargs)

    if response.status_code != 200:
        raise Exception(f'Request to {url} failed with status code {response.status_code}')

    if parse_as == "html":
        return BeautifulSoup(response.text, 'html.parser')
    elif parse_as == "json":
        return response.json()
    elif parse_as == "text":
        return response.text


# porting from old api
def getfilehost(url: str, hostname: bool = False) -> str:
    """
    Returns the file host or hostname of a URL.
    
    Parameters:
        url (str): The URL to get the file host or hostname from.
        hostname (bool): A flag indicating whether to return the hostname (True) or file host (False).
        
    Returns:
        str: The file host or hostname of the URL.
    """
    if hostname:
        return url.strip("/ ").split("/")[2]
    else:
        return url.strip("/ ").split("/")[-1]

def cleanurl(url: str, *args, **kwargs) -> str:
    """
    Cleans a URL by removing query parameters and other unnecessary elements.
    
    Parameters:
        url (str): The URL to clean.
        *args: Additional positional arguments to pass to the `url_query_cleaner` function.
        **kwargs: Additional keyword arguments to pass to the `url_query_cleaner` function.
        
    Returns:
        str: The cleaned URL.
    """
    return url_query_cleaner(url, *args, **kwargs)

def trailing(bs4, *, quotation_mark=False, apostrophe=False, combo=False):
    """
    Removes trailing characters from a string.

    Args:
        bs4 (str): The string to remove trailing characters from.
        quotation_mark (bool, optional): Removes quotation marks from the string. Defaults to False.
        apostrophe (bool, optional): Removes apostrophes from the string. Defaults to False.
        combo (bool, optional): Removes both quotation marks and apostrophes from the string. Defaults to False.

    Returns:
        str: The modified string.
    """
    if quotation_mark:
        return bs4.replace('"', '')
    if apostrophe:
        return bs4.replace("'", "")
    return bs4.replace("'", "").replace('"', ' ') if combo else bs4


def fix_annoy(bs4, double_newline=False, double_space=False, remove_part=None):
    """This function is intended for fixing some annoying parts of a string.

    Args:
        bs4 (str): The input string.
        double_newline (bool, optional): Fix double newline "a\ text \ b". Defaults to False.
        double_space (bool, optional): Fix double space like this "  a ". Defaults to False.
        remove_part (str, optional): A substring to remove from the input using a regular expression pattern. Defaults to None.

    Returns:
        str: The modified input string.
    """
    if double_newline:
        bs4 = bs4.replace('\n','').rstrip()
    if double_space and remove_part is None:
        bs4 = bs4.replace("  ", "")
    if remove_part is not None:
        bs4 = re.sub(remove_part, "", bs4)
        bs4 = bs4.lstrip()
    return bs4

def fix_url(url: str, *, clean=False, quote_plus=False, quote=False, quote_fix=False, unquote=False):
    """
    Fixes various issues with a URL.

    Args:
        url (str): The URL to fix.
        clean (bool, optional): Removes backslashes from the URL. Defaults to False.
        quote_plus (bool, optional): Encodes spaces and special characters in the URL using %20 and %XX. Defaults to False.
        quote (bool, optional): Encodes special characters in the URL using %XX. Defaults to False.
        quote_fix (bool, optional): Encodes the URL using %XX, with the exception of "/" and ":". Defaults to False.
        unquote (bool, optional): Decodes the URL using %XX. Defaults to False.

    Returns:
        str: The fixed URL.
    """
    if quote_fix:
        return urllib.parse.quote(url, safe="/:")
    elif unquote:
        return urllib.parse.unquote(url)
    elif quote_plus:
        return urllib.parse.quote_plus(url)
    elif quote:
        return urllib.parse.quote(url)
    elif clean:
        return url.replace("\\", "")
    else:
        return url


def extract_input_value(html, name):
    """Extracts the value of an input element with a specific name from an HTML string.

    Args:
        html (str): The HTML string.
        name (str): The name of the input element to search for.

    Returns:
        str: The value of the input element.
    """
    pattern = fr'<input.*?name="{name}".*?value="(.*?)".*?>'
    return match[1] if (match := re.search(pattern, html)) else ""

def extract_form_action(self, html):
    """Extracts the action attribute from a form element in an HTML string.

    Args:
        html (str): The HTML string.

    Returns:
        str: The value of the action attribute.
    """
    pattern = r'<form.*?action="(.*?)".*?>'
    return match.group(1) if (match := re.search(pattern, html)) else ""
    
def get_link_single(bs4: BeautifulSoup, attr: str, tag: str = None) -> Union[str, None]:
    """
    Extracts the specified attribute from an HTML element.

    Args:
        bs4: BeautifulSoup: a Beautiful Soup object representing an HTML element.
        attr: str: the name of the attribute to extract.
        tag: str: the name of the HTML tag to search for (optional).

    Returns:
        Union[str, None]: The value of the specified attribute of the first element with the specified tag that is found, if present. Returns None if no such element is found or if the attribute is not found.
    """
    element = bs4.find(tag) if tag else bs4
    return element.get(attr) if element else None


def get_title(bs4, generic=False, force=False, *args, **kwargs):
    """
    Extracts the title from an HTML element.

    Args:
        bs4: a Beautiful Soup object representing an HTML element.
        generic (bool, optional): Extracts the title using the "title" tag. Defaults to False.
        force (bool, optional): Extracts the text from the entire element, ignoring tags. Defaults to False.
        *args: Arguments passed to the `find` method of `bs4`.
        **kwargs: Keyword arguments passed to the `find` method of `bs4`.

    Returns:
        str: The title of the element.
    """
    if generic:
        return bs4.find("title").get_text()
    elif force:
        return bs4.get_text()
    else:
        return bs4.find(*args, **kwargs).get_text()
