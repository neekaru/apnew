from util.html.parser import fix_url

#  still in beta since i want grab some cookie
def get_cookie(cookie, *, debug=False, two=False, match=None, match1=None):
    """
    Extracts the Set-Cookie value from the headers of a request.

    Args:
        cookie: a request object.
        debug (bool, optional): Prints the Set-Cookie value for debugging purposes. Defaults to False.
        two (bool, optional): Extracts two Set-Cookie values. Defaults to False.
        match (int, optional): The index of the Set-Cookie value to extract. Defaults to None.
        match1 (int, optional): The index of the second Set-Cookie value to extract. Defaults to None.

    Returns:
        dict: A dictionary of Set-Cookie values.
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



def fix_cookie(cookie, *, default=False, quote=False, unquote=False):
    """
    Fixes a cookie by cleaning, quoting, or unquoting it.

    Args:
        cookie (any): The cookie to fix.
        default (bool, optional): Cleans the cookie by removing the ";" character. Defaults to False.
        quote (bool, optional): Quotes the cookie using the quote_plus function. Defaults to False.
        unquote (bool, optional): Unquotes the cookie using the unquote function. Defaults to False.

    Returns:
        any: The fixed cookie.
    """
    if default:
        return cookie.split(';')[0]
    elif quote:
        return fix_url(cookie, quote_plus=True)

    if unquote and default:
        return fix_url(cookie, unquote=True).split(';')[0]
    else:
        return fix_url(cookie, unquote=True)
