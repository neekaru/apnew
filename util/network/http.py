import cloudscraper
import requests

from util.utils import uegen

req = requests.session()

HEADER_DEFAULT: dict = {
    "User-Agent": uegen(default=True),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-us,en;q=0.6",
    "Sec-Fetch-Mode": "navigate",
}


def get_new_headers(
    additional_headers: dict[str, str] = None, edit_headers: dict[str, str] = None
) -> dict[str, str]:
    """
    Returns a dictionary of headers that includes the headers in `HEADER_DEFAULT` as well as the additional headers. The headers in `HEADER_DEFAULT` can be modified using the `edit_headers` parameter.

    Args:
        - additional_headers (Optional[Dict[str, str]]): A dictionary of additional headers to be included in the returned dictionary. Defaults to None.
        - edit_headers (Optional[Dict[str, str]]): A dictionary of headers to modify in `HEADER_DEFAULT`. The keys in this dictionary should match the keys in `HEADER_DEFAULT`, and the values will be used to update the corresponding values in `HEADER_DEFAULT`. Defaults to None.

    Returns:
        - Dict[str, str]: A dictionary of headers that includes the modified headers in `HEADER_DEFAULT` as well as the additional headers.
    """
    headers = HEADER_DEFAULT
    if edit_headers:
        headers.update(edit_headers)
    if additional_headers:
        headers.update(additional_headers)
    return headers


def cf():
    """
    just wannabe cf
    """
    reqcq = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    reqcq.headers.update(
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.6",
            "Sec-Fetch-Mode": "navigate",
        }
    )
    return reqcq


def starter(
    url: str, *, is_cf: bool = False, single: bool = False
) -> str | requests.Response | cloudscraper.requests.Response:
    """
    Makes a request to a website and disguises it as a visit by a real user.

    Args:
        url (str): The URL of the website.
        is_cf (bool, optional): Indicates whether the website has Cloudflare protection. Defaults to False.
        single (bool, optional): Makes a single request to the website without maintaining a session. Defaults to False.

    Returns:
        Union[str, requests.Response, cloudscraper.requests.Response]: The result of the request. This could be the status code or the response content.
    """
    if is_cf:
        reqcf = cf()
        return reqcf.get(url)

    headers = {
        "User-Agent": uegen(default=True),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-us,en;q=0.6",
        "Sec-Fetch-Mode": "navigate",
    }

    if single:
        return requests.get(url, headers=headers)

    return req.get(url, headers=headers)


def rpost(
    url: str, is_cf: bool = False, single: bool = False, *args, **kwargs
) -> cloudscraper.requests.Response | requests.Response | None:
    """
    Sends a POST request to the specified URL.

    Args:
        url (str): The URL to send the request to.
        is_cf (bool, optional): Set to True if the request is to a Cloudflare-protected page. Defaults to False.
        single (bool, optional): Set to True for a single request outside of a session. Defaults to False.
        *args: Additional arguments to pass to the request function.
        **kwargs: Additional keyword arguments to pass to the request function.

    Returns:
        Union[cloudscraper.requests.Response, requests.Response, None]: The response to the request, or None if the request failed.
    """
    if is_cf:
        reqcf = cf()
        return reqcf.post(url, *args, **kwargs)

    if single:
        return requests.post(url, *args, **kwargs)

    return req.post(url, *args, **kwargs)


def rget(
    url: str, is_cf: bool = False, single: bool = False, *args, **kwargs
) -> cloudscraper.requests.Response | requests.Response | None:
    """
    Sends a GET request to the specified URL.

    Args:
        url (str): The URL to send the request to.
        is_cf (bool, optional): Set to True if the request is to a Cloudflare-protected page. Defaults to False.
        single (bool, optional): Set to True for a single request outside of a session. Defaults to False.
        *args: Additional arguments to pass to the request function.
        **kwargs: Additional keyword arguments to pass to the request function.

    Returns:
        Union[cloudscraper.requests.Response, requests.Response, None]: The response to the request, or None if the request failed.
    """
    if is_cf:
        reqcf = cf()
        return reqcf.get(url, *args, **kwargs)

    if single:
        return requests.get(url, *args, **kwargs)

    return req.get(url, *args, **kwargs)
