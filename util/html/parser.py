from typing import Union
from bs4 import BeautifulSoup
from w3lib.url import url_query_cleaner
import urllib.parse, re


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
    if combo:
        return bs4.replace("'", "").replace('"', ' ')
    return bs4


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
    match = re.search(pattern, html)
    if match:
        return match.group(1)
    return ""
    
def get_link_single(bs4: BeautifulSoup, attr: str, tag: str = None) -> Union[str, None]:
    """
    Extracts the specified attribute from an HTML element.

    Args:
        bs4: BeautifulSoup: a Beautiful Soup object representing an HTML element.
        attr: str: the name of the attribute to extract (must be "href" or "src").
        tag: str: the name of the HTML tag to search for (optional).

    Returns:
        Union[str, None]: The value of the specified attribute of the first element with the specified tag that is found, if present. Returns None if no such element is found or if the attribute is not found.
    """
    if attr not in ("href", "src"):
        raise ValueError("Attribute must be 'href' or 'src'")

    if tag:
        element = bs4.find(tag)
    else:
        element = bs4

    if element:
        return element.get(attr)
    return None





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
