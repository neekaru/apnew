import json
import re
import codecs
from typing import Any, List, Union, Dict
from bs4 import BeautifulSoup, Tag
from urllib.parse import quote as quot
from urllib.parse import quote_plus as quot_plus
from urllib.parse import unquote as unquot
from urllib.parse import urlparse
from w3lib.url import url_query_cleaner
from util.network.http import rget, rpost


class GetHtml(BeautifulSoup):
    def __init__(
        self, url: str
    ):
        self.url = url

    def get_bs4(self) -> BeautifulSoup | None:
        """
        Returns a Beautiful Soup object from an HTML string.

        Args:
            url (str): The HTML string.

        Returns:
            Union[BeautifulSoup, None]: A Beautiful Soup object, or None if the HTML string is invalid.
        """
        try:
            return BeautifulSoup(self.url, "html.parser")
        except Exception:
            return None

    def download_webpage_with_post(
        self,
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
            response = rpost(
                self.url, headers=headers, is_cf=True, data=data, *args, **kwargs
            )
        elif single:
            response = rpost(
                self.url, headers=headers, single=True, data=data, *args, **kwargs
            )
        else:
            response = rpost(self.url, headers=headers, data=data, *args, **kwargs)

        if response.status_code != 200:
            raise Exception(
                f"Request to {self.url} failed with status code {response.status_code}"
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
        self,
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
            response = rget(self.url, headers=headers, is_cf=True, *args, **kwargs)
        elif single:
            response = rget(self.url, headers=headers, single=True, *args, **kwargs)
        else:
            response = rget(self.url, headers=headers, *args, **kwargs)

        if response.status_code != 200:
            raise Exception(
                f"Request to {self.url} failed with status code {response.status_code}"
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


class parser(GetHtml):
    def __init__(self, html = None, json: dict = None, js: str = None):
        self.html = html
        self.json = json
        self.js = js
        self.bs4: BeautifulSoup

    def extract_from_list(self, lst, tag_name, attr=None):
        result = []
        for item in lst:
            if isinstance(item, Tag):
                if attr:
                    result.append(item.get(attr))
                else:
                    result.append(item.get_text())
            else:
                soup = self.bs4(str(item), "html.parser")
                tags = soup.find_all(tag_name)
                for tag in tags:
                    if attr:
                        result.append(tag.get(attr))
                    else:
                        result.append(tag.get_text())
        return result

    def find_or_find_all(
        self, find_all: bool = False, *args, **kwargs
    ):
        if find_all:
            return self.bs4.find_all(self.html, *args, **kwargs)
        else:
            return self.bs4.find(self.html, *args, **kwargs)

    def select_or_select_all(
        self, select_all: bool = False, *args, **kwargs
    ):
        if select_all:
            return self.bs4.select(self.html, *args, **kwargs)
        else:
            return self.bs4.select_one(self.html, *args, **kwargs)

    def extract_input_value(self, name: str) -> str:
        pattern = rf'<input.*?name="{name}".*?value="(.*?)".*?>'
        return match.group(1) if (match := re.search(pattern, self.html)) else ""

    @staticmethod
    def extract_form_data(form) -> Dict[str, str]:
        """Extracts data from a form element.

        Returns:
            A dictionary mapping form input names to their values.
        """
        data = {}
        for input_element in form.find_all("input"):
            name = input_element.get("name")
            value = input_element.get("value")
            data[name] = value
        return data

    def extract_json_data(self: dict, keys: list) -> dict:
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
            if key in self.json and self.json[key] not in (None, ""):
                extracted_data[key] = self.json[key]
        return extracted_data

    def js_to_json(self: str) -> dict:
        # Find the JSON object in the JavaScript string using a regular expression
        match = re.search(r"\{.*\}", self.js)
        if match:
            # Extract the JSON object and parse it into a Python dictionary
            json_str = match.group(0)
            return json.loads(json_str)
        else:
            return {}


class clean:
    def __init__(self, url) -> None:
        self.url = url

    def cleanurl(self, *args, **kwargs) -> str:
        """
        Cleans a URL by removing query parameters and other unnecessary elements.

        Parameters:
            url (Any): The URL to clean.
            *args: Additional positional arguments to pass to the `url_query_cleaner` function.
            **kwargs: Additional keyword arguments to pass to the `url_query_cleaner` function.

        Returns:
            str: The cleaned URL.
        """
        return url_query_cleaner(self.url, *args, **kwargs)

    # porting from old api
    def getfilehost(self, hostname: bool = False) -> str:
        """
        Returns the file host or hostname of a URL.

        Parameters:
            url (Any): The URL to get the file host or hostname from.
            hostname (bool): A flag indicating whether to return the hostname (True) or file host (False).

        Returns:
            str: The file host or hostname of the URL.
        """
        parsed_url = urlparse(self.url)
        if hostname:
            return parsed_url.hostname
        else:
            return parsed_url.path.strip("/ ").split("/")[-1]

    def fix_url(
        self,
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
            clean (bool, optional): Removes backslashes from the URL. Defaults to False.
            quote_plus (bool, optional): Encodes spaces and special characters in the URL using %20 and %XX. Defaults to False.
            quote (bool, optional): Encodes special characters in the URL using %XX. Defaults to False.
            quote_fix (bool, optional): Encodes the URL using %XX, with the exception of "/" and ":". Defaults to False.
            unquote (bool, optional): Decodes the URL using %XX. Defaults to False.

        Returns:
            Union[str, None]: The fixed URL, or None if the URL is invalid.
        """
        if quote_fix:
            return quot(str(self.url), safe="/:")
        elif unquote:
            return unquot(self.url)
        elif quote_plus:
            return quot_plus(self.url)
        elif quote:
            return quot(self.url)
        elif clean:
            return self.url.replace("\\", "")
        else:
            return self.url


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
