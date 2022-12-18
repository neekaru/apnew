from util.html.parser import fix_url

#  still in beta since i want grab some cookie
def get_cookie(cookie, debug: bool = False, two: bool = False, match: int = 0, match1: int = 0):
    """This intended for able to grab set-cookie in header of requests
    because some website need you to serve them some cookies

    Args:
        cookie (any): this for grabbing from requests
        debug (bool, optional): This is intended as debugging header to grab cookie. Defaults to False.
        two (bool, optional): This for if you want grab two cookie. Defaults to False.
        match (int, optional): For Grabbing One cookie in list. Defaults to None.
        match1 (int, optional): For Grabbing Two Cookie in list. Defaults to None.

    Returns:
        dict: a array of coookie
    """
    if two:
        pas1 = cookie.headers['Set-Cookie'].split(" ")[match]
        pas2 = cookie.headers['Set-Cookie'].split(" ")[match1]
        return pas1, pas2
    if debug:
        return cookie.headers['Set-Cookie'].split(" ")
    else: 
        pas = cookie.headers['Set-Cookie'].split(" ")[match]
    return pas


def fix_cookie(cookie, default: bool = False, quote: bool = False, unquote: bool = False):
    """This is intend to able to Fix some cookie due to some website have a trick 
    to detect bot or not by checking how they serve cookie

    Args:
        cookie (any): a cookie
        default (bool, optional): This if you want only cleaning ";" in your cookies. Defaults to False.
        quote (bool, optional): This for quoting the cookie. Defaults to False.
        unquote (bool, optional): This for unquote the cookie. Defaults to False.

    Returns:
        any: a fixed cookie
    """
    if default:
        return cookie.split(';')[0]
    elif quote:
        return fix_url(cookie, quote_plus=True)

    if unquote and default:
        return fix_url(cookie, unquote=True).split(';')[0]
    else:
        return fix_url(cookie, unquote=True)