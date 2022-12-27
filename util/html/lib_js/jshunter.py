from __future__ import unicode_literals
import re

_0xce1e = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"


class log_error(Exception):
    """Badly packed source or general error. Argument is a
    meaningful description."""


def duf(d, e, f):
    g = list(_0xce1e)
    h = g[:e]
    i = g[:f]
    d = list(d)[::-1]
    j = 0
    for c, b in enumerate(d):
        if b in h:
            j = j + h.index(b) * e**c

    k = ""
    while j > 0:
        k = i[j % f] + k
        j = (j - (j % f)) // f

    return int(k) or 0


def hunter(h, u, n, t, e, r):
    r = ""
    i = 0
    while i < len(h):
        j = 0
        s = ""
        while h[i] is not n[e]:
            s = "".join([s, h[i]])
            i += 1

        while j < len(n):
            s = s.replace(n[j], str(j))
            j = j + 1

        r = "".join([r, "".join(map(chr, [duf(s, e, 10) - t]))])
        i += 1

    return r


def unpack_js(code: str) -> str:
    # sourcery skip: inline-immediately-returned-variable
    """
    Unpacks the JavaScript code.

    :param code: The JavaScript code to be unpacked.
    :return: The unpacked JavaScript code, or None if the code couldn't be unpacked.
    """
    try:
        # Extract the arguments for the hunter function from the code
        regex = r"\(\"([^)]+)\)"
        matches = re.findall(regex, code, re.MULTILINE)[0]
        code_list = matches.split(',')
        for idx, code in enumerate(code_list):
            code_list[idx] = int(code) if code.isdigit() else code.replace('\"', '')
        # Call the hunter function with the extracted arguments
        result = hunter(*code_list)
        return result
    except Exception as e:
        log_error()
    return None
