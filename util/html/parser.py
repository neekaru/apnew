import codecs
import json
import re
from typing import Any
from urllib.parse import quote as quot
from urllib.parse import quote_plus as quot_plus
from urllib.parse import unquote as unquot
from urllib.parse import urlparse

import defusedxml
from bs4 import BeautifulSoup
from bs4.element import Tag
from w3lib.url import url_query_cleaner

from util.network.http import rget, rpost


def get_bs4(url: str) -> BeautifulSoup | None:
    """
    Returns a Beautiful Soup object from an HTML string.

    Args:
        url (str): The HTML string.

    Returns:
        Union[BeautifulSoup, None]: A Beautiful Soup object, or None if the HTML string is invalid.
    """
    try:
        return BeautifulSoup(url, "html.parser")
    except Exception:
        return None


def download_webpage_with_post(
    url: str = None,
    headers: dict[str, str] = None,
    cf: bool = False,
    single: bool = False,
    data: dict[str, Any] = None,
    response_option: str = "Normal",
    parse_as: str = "html",
    *args,
    **kwargs,
) -> BeautifulSoup | str | dict[str, Any]:
    """
    Downloads and optionally parses the response of a webpage using a POST request.

    Parameters:
        url (str): The URL of the webpage to download. If not provided, the URL will be taken from the `headers` argument.
        headers (Dict[str, str]): A dictionary of HTTP headers to send with the request. If not provided, the `url` argument will be used as the URL.
        cf (bool): A flag indicating whether to use the cloudscraper on requests.post() function which can handles Cloudflare protection.
        single (bool): A flag if you want use single requests not session.
        data (Dict[str, Any]): A dictionary of data to send in the body of the request.
        response_option (str): A flag indicating what to return from the function. Can be "Normal" (the parsed response), "url", or "headers". If not provided, the function will return the parsed response based on the value of the `parse_as` argument.
        parse_as (str): A string indicating how to parse the response. Can be "html", "text", "Nothing" or "json". If not provided, the function will return the parsed response based on the value of the `response_option` argument.
        *args: Additional positional arguments to pass to the requests.post() or cf() function.
        **kwargs: Additional keyword arguments to pass to the requests.post() or cf() function.

    Returns:
        Union[BeautifulSoup, str, dict[str, Any]]: A BeautifulSoup object containing the parsed HTML of the webpage, the raw response text as a string, or the response JSON data as a dictionary, depending on the value of `parse_as`.

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
        raise Exception(
            f"Request to {url} failed with status code {response.status_code}"
        )

    # If the response_option argument is provided, return the appropriate value
    if response_option:
        if response_option == "Normal":
            if parse_as:
                if parse_as == "html":
                    return BeautifulSoup(response.text, "html.parser")
                elif parse_as == "json":
                    return response.json()
                elif parse_as == "text":
                    return response.text
        elif response_option == "headers":
            return response.headers
        elif response_option == "url":
            return response.url
        else:
            return response
    elif parse_as:
        if parse_as == "html":
            return BeautifulSoup(response.text, "html.parser")
        elif parse_as == "json":
            return response.json()
        elif parse_as == "text":
            return response.text
    else:
        return response


def download_webpage(
    url: str = None,
    headers: dict[str, str] = None,
    cf: bool = False,
    single: bool = False,
    response_option: str = "Normal",
    parse_as: str = "html",
    *args,
    **kwargs,
) -> BeautifulSoup | str | dict[str, str]:
    """
    Downloads and parses the HTML of a webpage.

    Parameters:
        url (str): The URL of the webpage to download. If not provided, the URL will be taken from the `headers` argument.
        headers (Dict[str, str]): A dictionary of HTTP headers to send with the request. If not provided, the `url` argument will be used as the URL.
        cf (bool): A flag indicating whether to use the cloudscraper on requests.get() function which can handles Cloudflare protection.
        single (bool): A flag if you want use single requests not session.
        response_option (str): A flag indicating what to return from the function. Can be "Normal" (the parsed response), "url", or "headers". If not provided, the function will return the parsed response based on the value of the `parse_as` argument.
        parse_as (str): A string indicating how to parse the response. Can be "html", "text", "Nothing" or "json". If not provided, the function will return the parsed response based on the value of the `response_option` argument.
        *args: Additional positional arguments to pass to the requests.get() or cf() function.
        **kwargs: Additional keyword arguments to pass to the requests.get() or cf() function.

    Returns:
        Union[BeautifulSoup, str, dict[str, str]]: The parsed response, URL, or headers of the webpage, depending on the value of the `response_option` or `parse_as` argument.

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
        raise Exception(
            f"Request to {url} failed with status code {response.status_code}"
        )

    # If the response_option argument is provided, return the appropriate value
    if response_option:
        if response_option == "Normal":
            if parse_as:
                if parse_as == "html":
                    return BeautifulSoup(response.text, "html.parser")
                elif parse_as == "json":
                    return response.json()
                elif parse_as == "text":
                    return response.text
        elif response_option == "headers":
            return response.headers
        elif response_option == "url":
            return response.url
        else:
            return response
    elif parse_as:
        if parse_as == "html":
            return BeautifulSoup(response.text, "html.parser")
        elif parse_as == "json":
            return response.json()
        elif parse_as == "text":
            return response.text
    else:
        return response


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
    parsed_url = urlparse(url)
    if hostname:
        return parsed_url.hostname
    else:
        return parsed_url.path.strip("/ ").split("/")[-1]


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


def trailing(
    bs4: str,
    *,
    quotation_mark: bool = False,
    apostrophe: bool = False,
    combo: bool = False,
) -> str:
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
        return bs4.replace('"', "")
    if apostrophe:
        return bs4.replace("'", "")
    return bs4.replace("'", "").replace('"', " ") if combo else bs4


def find_element_by_css_selector(
    html: str,
    selector: str,
    method: str = "css",
    single: bool = False,
    parse_html: bool = True,
) -> list[Tag] | Tag:
    # sourcery skip: assign-if-exp, switch
    """
    Find that needle in the haystack! This function helps you locate an HTML element (or elements) within an HTML document using a CSS selector or XPath expression.

    Args:
    - html (str): The HTML document as a string. Think of it as the haystack where you'll be searching for the needle (the element).
    - selector (str): The CSS selector or XPath expression to use for element selection. This is the needle that will help you find the element(s) you're looking for.
    - method (str, optional): The method to use for element selection. Can be either "css" or "xpath". Defaults to "css".
    - single (bool, optional): Whether to return a single element or a list of elements. Defaults to False (return a list).
    - parse_html (bool, optional): Whether to parse the HTML document using Beautiful Soup. Defaults to True.

    Returns:
    - Union[List[Tag], Tag]: A list of Beautiful Soup Tag objects if single is False, or a single Tag object if single is True.
    """

    # Parse the HTML document
    if parse_html:
        soup = BeautifulSoup(html, "html.parser")
    root = defusedxml.fromstring(
        html
    )  # use defusedxml.fromstring instead of etree.fromstring

    # Find the element(s) using the specified method
    if method == "css":
        if single:
            elements = soup.select_one(selector)
        else:
            elements = soup.select(selector)
    elif method == "xpath":
        if single:
            elements = root.xpath(selector)
        else:
            elements = root.xpath(f"/{selector}")
    else:
        raise ValueError('Invalid method. Choose "css" or "xpath".')

    # Return the element(s)
    return elements


def fix_annoy(
    bs4: str,
    double_newline: bool = False,
    double_space: bool = False,
    remove_part: str | None = None,
    unicode_escape: bool | None = None,
    weird_unicode_remover: bool | None = None,
) -> str:
    """
    Fixes annoying parts of a string.

    Parameters:
    -   string (str): The input string to be modified.
    -   fix_double_newlines (bool): If True, fix double newlines in the input string (e.g. "a   text  b"), Defaults to False.
    -   fix_double_spaces (bool): If True, fix double spaces in the input string (e.g. " a "), Defaults to False.
    -   remove_substring (str): A substring to remove from the input using a regular expression pattern, Defaults to None.
    -   decode_unicode (bool): If True, decode the input string using the "unicode_escape" codec, Defaults to None.
    -   remove_weird_unicode (bool): If True, remove non-ASCII characters from the input string, Defaults to None.

    Returns:
        str: The modified input string.
    """
    if double_newline:
        bs4 = bs4.replace("\n", "").rstrip()
    if double_space and remove_part is None:
        bs4 = bs4.replace("  ", "")
    if remove_part is not None:
        bs4 = re.sub(remove_part, "", bs4)
        bs4 = bs4.lstrip()
    if unicode_escape is not None:
        return codecs.decode(bs4, "unicode_escape")
    if weird_unicode_remover is not None:
        return re.sub(r"[^\x00-\x7F]", "", bs4)
    return bs4


def fix_url(
    url: str,
    *,
    clean: bool = False,
    quote_plus: bool = False,
    quote: bool = False,
    quote_fix: bool = False,
    unquote: bool = False,
) -> str | None:
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
        Union[str, None]: The fixed URL, or None if the URL is invalid.
    """
    if quote_fix:
        return quot(str(url), safe="/:")
    elif unquote:
        return unquot(url)
    elif quote_plus:
        return quot_plus(url)
    elif quote:
        return quot(url)
    elif clean:
        return url.replace("\\", "")
    else:
        return url


def extract_input_value(html: str, name: str) -> str:
    """
    Extracts the value of an input element with a specific name from an HTML string.

    Args:
        html (str): The HTML string.
        name (str): The name of the input element to search for.

    Returns:
        str: The value of the input element.
    """
    pattern = rf'<input.*?name="{name}".*?value="(.*?)".*?>'
    return match.group(1) if (match := re.search(pattern, html)) else ""


def extract_form_data(form) -> dict[str, str]:
    """Extracts data from a form element.

    Args:
        form: The form element to extract data from.

    Returns:
        A dictionary mapping form input names to their values.
    """
    data = {}
    for input_element in form.find_all("input"):
        name = input_element.get("name")
        value = input_element.get("value")
        data[name] = value
    return data


def extract_json_data(json_data: dict, keys: list) -> dict:
    """
    Extracts data from a JSON object using a list of keys.

    Args:
        json_data (dict): The JSON object.
        keys (list): The keys to extract.

    Returns:
        dict: A dictionary containing the extracted data.
    """
    extracted_data = {}
    for key in keys:
        if key in json_data and json_data[key] not in (None, ""):
            extracted_data[key] = json_data[key]
    return extracted_data


def js_to_json(js: str) -> dict:
    # Find the JSON object in the JavaScript string using a regular expression
    match = re.search(r"\{.*\}", js)
    if match:
        # Extract the JSON object and parse it into a Python dictionary
        json_str = match.group(0)
        return json.loads(json_str)
    else:
        return {}


def extract_data_regex(
    html: str, preset: str = None, pattern: str = None, group: int = 0
) -> str:
    """
    Extracts data from an HTML string using a regular expression.

    Args:
        html (str): The HTML string.
        preset (str): The name of a preset regular expression pattern to use (optional).
        pattern (str): A custom regular expression pattern to use (optional).
        group (int): The group number to extract (optional).

    Returns:
        str: The data that matches the regular expression pattern. Returns an empty string if no match is found.
    """
    if preset == "form_action":
        pattern = r'<form.*?action="(.*?)".*?>'
    elif preset == "a_href":
        pattern = r'<a.*?href="(.*?)".*?>'
    elif pattern is None:
        raise ValueError("Either a preset or a custom pattern must be specified.")

    match = re.search(pattern, html)
    return match.group(group) if match else ""


def get_link_or_title(
    bs4: BeautifulSoup,
    attr: str = None,
    tag: str = None,
    css: str = None,
    multiple: bool = False,
    raw: bool = False,
    force_text: bool = False,
    process=None,
    *args,
    **kwargs,
) -> str | list[str] | dict[str, str]:
    # sourcery skip: assign-if-exp, merge-else-if-into-elif
    """
    Extracts specified data from an HTML element or form.

    Parameters:
        element (bs4.BeautifulSoup): A Beautiful Soup object representing an HTML element or form.
        data_type (str): The name of the data to extract (optional). Can be "attribute" or "title".
        tag (str): The name of the HTML tag to search for (optional).
        css (str): A CSS selector to search for (optional).
        multiple (bool): Indicates whether to extract data from multiple elements (optional).
        raw (bool): Indicates whether to return the raw HTML or the text content of the element or elements (optional).
        force_text (bool): Indicates whether to force the extraction of the text content of the element or elements, regardless of the value of raw (optional).
        process (Callable): A processing function to apply to the extracted data (optional).
        *args: Arguments passed to the find or find_all method of element.
        **kwargs: Keyword arguments passed to the find or find_all method of element.

    Returns:
    Union[str, List[str], dict[str, str]]: The value of the specified data of the first element with the specified tag or matching the CSS selector that is found, if present. Returns a list of values if multiple is True. Returns a dictionary mapping form input names to their values if element is a form element. Returns None if no such element is found or if the data is not found.
    """
    if tag == "form":
        element = bs4.find(tag, *args, **kwargs)
        return extract_form_data(element)
    else:
        if css:
            if multiple:
                elements = bs4.select(css)
            else:
                element = bs4.select_one(css)
        else:
            if multiple:
                elements = bs4.find_all(tag, *args, **kwargs)
            else:
                element = bs4.find(tag, *args, **kwargs)

        if multiple:
            if raw and not force_text:
                data = [str(element) for element in elements]
            else:
                if attr and not force_text:
                    data = [element.get(attr) for element in elements]
                else:
                    data = [element.get_text() for element in elements]
        else:
            if element:
                if raw and not force_text:
                    data = str(element)
                else:
                    if attr and not force_text:
                        data = element.get(attr)
                    else:
                        data = element.get_text()
            else:
                return None
        if process:
            data = process(data)
        return data
