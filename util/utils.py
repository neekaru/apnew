from .html.genua import GenerateMobileUseragent, GetRandomUserAgent
import requests, re
from fake_useragent import UserAgent

def fix_link(url):
    """This Intended For fix some link because some website
    Only Support long link rather than short link

    Args:
        url (str): Give Your Link
    """
    return requests.get(url).url

def clean_http(captions, newline=False):
    """This for cleaning https or http on caption

    Args:
        captions (str): for cleaning the url and https

    Returns:
        str: a result
    """
    if newline:
        d2 = re.sub(r"https?://\S+", "", captions)
        caption = re.sub(r'\t+', '', d2)
        caption = re.sub(r'\n', '', d2)
    else:
        d2 = re.sub(r"https?://\S+", "", captions)
        caption = re.sub(r'\t+', '', d2)
    return caption

def uegen(default: bool = False, mobile: bool = False, random: bool = False, alter: bool = False, spesific: list[str] = None):
    """
    uegen aka Useragent Generator
    This need because some website detect bot or not by checking the user-agent of the request

    Args:
        default (bool, optional): For generate legit useragent. Defaults to False.
        random (bool, optional): If you want generate some random useragent. Defaults to False.
        alter (bool, optional): For Alternative way same as random but is for if you want minimal. Defaults to False.
        spesific (list[str], optional): If you want specific way like [edge, chrome]. Defaults to None.

    Returns:
        str: a string of useragent
    """
    
    if default:
        return GetRandomUserAgent()
    elif mobile:
        return GenerateMobileUseragent()

    if random:
        ua = UserAgent(browsers=['firefox', 'edge', 'safari', 'chrome'], use_external_data=True)
        return ua.random
    elif alter:
        ua = UserAgent(browsers=['edge', 'chrome'])
        return ua.random

    if spesific is None:
        spesific = []
    elif spesific:
        ua1 = UserAgent(browsers=[spesific])
        return ua1.random

def csrfget(bs4, middleware: bool = False, csrf: bool = False):
    if middleware:
        return bs4.find("input", {"name": "csrfmiddlewaretoken"}).get("value")
    if csrf:
        return None