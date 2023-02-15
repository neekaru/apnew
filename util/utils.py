import base64
import binascii
import contextlib
import datetime
import re

import humanize
import requests
from fake_useragent import UserAgent

from util.html.genua import GenerateMobileUseragent, GetRandomUserAgent

from .html import parser


def fix_link(url: str) -> str:
    """
    Fixes a shortened URL by expanding it.

    Args:
        url (str): The shortened URL.

    Returns:
        str: The expanded URL.
    """
    return requests.get(url).url


def clean_string(captions: str, *, newline: bool | None = False) -> str:
    """
    Removes HTTP and HTTPS links, newline characters, and tab characters from a string.

    Args:
        captions (str): The string to clean.
        newline (bool, optional): Removes newline characters as well. Defaults to False.

    Returns:
        str: The cleaned string.
    """
    # Remove HTTP and HTTPS links, newline characters, and tab characters
    pattern = r"(https?://\S+|\n|\t+)" if newline else r"(https?://\S+|\t+)"
    return re.sub(pattern, "", captions)


def uegen(
    *,
    default: bool | None = False,
    mobile: bool | None = False,
    random: bool | None = False,
    alter: bool | None = False,
    spesific: list[str] | None = None,
) -> str:
    """
    Generates a user agent string.

    Args:
        default (bool, optional): Generates a legit user agent. Defaults to False.
        mobile (bool, optional): Generates a mobile user agent. Defaults to False.
        random (bool, optional): Generates a random user agent. Defaults to False.
        alter (bool, optional): Generates a minimal random user agent. Defaults to False.
        spesific (List[str], optional): Generates a user agent for a specific browser. Defaults to None.

    Returns:
        str: A user agent string.
    """
    if default:
        return GetRandomUserAgent()
    elif mobile:
        return GenerateMobileUseragent()

    if random:
        ua = UserAgent(
            browsers=["firefox", "edge", "safari", "chrome"], use_external_data=False
        )
        return ua.random
    elif alter:
        ua = UserAgent(browsers=["edge", "chrome"])
        return ua.random

    if spesific is None:
        spesific = []
    elif spesific:
        ua1 = UserAgent(browsers=[spesific])
        return ua1.random
    return ""


def csrfget(
    bs4, *, middleware: bool | None = False, csrf: bool | None = False
) -> str | None:
    """
    Extracts the CSRF token from an HTML element.

    Args:
        bs4: a Beautiful Soup object representing an HTML element.
        middleware (bool, optional): Extracts the CSRF token using the "csrfmiddlewaretoken" input. Defaults to False.
        csrf (bool, optional): Extracts the CSRF token using the "csrf" input. Defaults to False.

    Returns:
        Optional[str]: The CSRF token, or None if no token could be found.
    """
    if middleware:
        return parser.get_link_or_title(
            bs4, tag="input", attr="value", args={"name": "csrfmiddlewaretoken"}
        )
    if csrf:
        return None


def get_readable_time(
    seconds: int | float, unix_epoch: bool = False, utc: bool = False
) -> str:
    """
    Return a human-readable time format in the format %dd %hh %mm %ss.

    Args:
        seconds (Union[int, float]): The number of seconds to convert to a human-readable format. The value can be an
                                    integer or a float.
        unix_epoch (bool, optional): If set to True, the given seconds value will be interpreted as a Unix timestamp and
                                     converted to the equivalent time based on the Unix epoch (default is False).
        utc (bool, optional): If set to True, the calculated time will be converted to the equivalent time in the
                              Coordinated Universal Time (UTC) time zone (default is False).

    Returns:
        str: The human-readable time format.
    """
    if unix_epoch:
        # If the unix_epoch argument is set to True, we need to convert the given seconds value to the equivalent
        # time based on the Unix epoch.
        return humanize.naturaltime(
            datetime.datetime.fromtimestamp(
                seconds, tz=datetime.timezone.utc if utc else None
            )
        )
    else:
        # If the unix_epoch argument is not set, we can use the given seconds value to create a datetime object
        # representing the current date and time, and then subtract or add the number of seconds from/to it to get the
        # desired time.
        if seconds < 0:
            # If the seconds value is negative, subtract the number of seconds from the current date and time.
            time = datetime.datetime.now(
                tz=datetime.timezone.utc if utc else None
            ) - datetime.timedelta(seconds=abs(seconds))
        else:
            # If the seconds value is positive, add the number of seconds to the current date and time.
            time = datetime.datetime.now(
                tz=datetime.timezone.utc if utc else None
            ) + datetime.timedelta(seconds=seconds)

        return humanize.naturaltime(time)


def get_readable_size(size: int) -> str | None:
    """
    Return a human-readable size format.

    This function converts the given size in bytes to a human-readable format,
    such as "1.23 MiB" for megabytes.

    Args:
        size (int): The size in bytes to convert to a human-readable format.

    Returns:
        Union[str, None]: The size in a human-readable format, or None if the size is 0.
    """
    if not size:
        return None
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}

    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}B"


def detect_string_type(string: str) -> str | None:
    """Determine the type of the given string.

    This function is intended for detecting the type of a hash or encoded string.

    Args:
        string (str): The string to detect the type of.

    Returns:
        Union[str, None]: The type of the string, or None if the type could not be determined.
    """
    if all(c.isdigit() for c in string):
        return "hex"
    elif len(string) in {32, 40, 56, 64, 96, 128}:
        return {
            32: "md5",
            40: "sha1",
            56: "sha224",
            64: "sha256",
            96: "sha384",
            128: "sha512",
        }[len(string)]
    elif all(c in string.ascii_letters + string.digits + "+/=" for c in string):
        with contextlib.suppress(Exception):
            # Decode the string using base64
            base64.b64decode(string)
            return "base64"
    return None


def decode_string(encoded_string: str, encoding: str) -> str:
    """
    Decodes the given encoded string using the specified encoding.

    Parameters:
        encoded_string (str): The encoded string to decode.
        encoding (str): The encoding method to use for decoding. Supported values are:
            - "utf-8" (default): Decodes the string using the UTF-8 encoding.
            - "base64": Decodes the string using the base64 encoding.
            - "hex": Decodes the string using the hexadecimal encoding.

    Returns:
        str: The decoded string.
    """
    if encoding == "base64":
        return base64.b64decode(encoded_string).decode("utf-8")
    elif encoding == "hex":
        return binascii.unhexlify(encoded_string).decode("utf-8")
    else:
        return encoded_string.decode(encoding)
