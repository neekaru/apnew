import re

def log_error(e: Exception):
    """
    Logs an error message.

    :param e: The exception to be logged.
    """
    return f"Error Because{e}"

class StringBuilder:
    def __init__(self, string=""):
        self.string = string
    
    def append(self, string):
        self.string += string
    
    def to_string(self):
        return self.string

# unpacked
class Unbase:
    def __init__(self, radix: int):
        self.alphabet = None
        self.dictionary = None
        if radix > 36:
            if radix < 62:
                self.alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[:radix]
            elif 63 <= radix <= 94:
                self.alphabet = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"[:radix]
            elif radix == 62:
                self.alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            elif radix == 95:
                self.alphabet = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
            self.dictionary = {}
            for i in range(len(self.alphabet)):
                self.dictionary[self.alphabet[i]] = i

    def unbase(self, s: str) -> int:
        ret = 0
        if self.alphabet is None:
            ret = int(s, radix=self.radix)
        else:
            tmp = s[::-1]
            for i in range(len(tmp)):
                ret += (self.radix ** i) * self.dictionary[tmp[i]]
        return ret


# https://github.com/cylonu87/JsUnpacker
class JsUnpacker:
    def __init__(self, packed_js: str):
        self.packed_js = packed_js

    def detect(self) -> bool:
        """
        Detects whether the JavaScript is P.A.C.K.E.R coded.

        :return: True if the JavaScript is P.A.C.K.E.R coded, False otherwise.
        """
        js = self.packed_js.replace(" ", "")
        pattern = re.compile(r"eval\(function\(p,a,c,k,e,[rd]")
        match = pattern.search(js)
        return match is not None

    def unpack(self) -> str:
        """
        Unpacks the JavaScript code.

        :return: The unpacked JavaScript code, or None if the code couldn't be unpacked.
        """
        js = self.packed_js
        try:
            pattern = re.compile(r"""\}\s*\('(.*)',\s*(.*?),\s*(\d+),\s*'(.*?)'\.split\('\|'\)""", re.DOTALL)
            match = pattern.search(js)
            if match and match.group(4) is not None:
                payload = match.group(1).replace("\\'", "'")
                radix_str = match.group(2)
                count_str = match.group(3)
                symtab = match.group(4).split("\\|")
                radix = 36
                count = 0
                try:
                    radix = int(radix_str)
                except Exception:
                    pass
                try:
                    count = int(count_str)
                except Exception:
                    pass
                if len(symtab) != count:
                    raise Exception("Unknown p.a.c.k.e.r. encoding")
                unbase = Unbase(radix)
                pattern = re.compile(r"\b\w+\b")
                match = pattern.search(payload)
                decoded = StringBuilder(payload)
                replace_offset = 0
                while match:
                    word = match.group(0)
                    x = unbase.unbase(word)
                    value = None
                    if 0 <= x < len(symtab):
                        value = symtab[x]
                    if value and value:
                        decoded.replace(
                            match.start() + replace_offset,
                            match.end() + replace_offset,
                            value,
                        )
                        replace_offset += len(value) - len(word)
                    match = pattern.search(payload, match.end())
                return decoded.to_string()
        except Exception as e:
            log_error(e)
        return None

class JsHunter:
    """
    A class for detecting and unpacking H.U.N.T.E.R-coded JavaScript.
    """
    def __init__(self, hunter_js: str):
        """
        Initializes a new instance of the JsHunter class with the given JavaScript code.

        :param hunter_js: The JavaScript code to be processed.
        """
        self.hunter_js = hunter_js

    def detect(self) -> bool:
        """
        Detects whether the JavaScript code is H.U.N.T.E.R coded.

        :return: True if the JavaScript code is H.U.N.T.E.R coded, False otherwise.
        """
        pattern = re.compile(r"eval\(function\(h,u,n,t,e,r\)")
        search_results = pattern.search(self.hunter_js)
        return search_results is not None

    def dehunt(self) -> str:
        """
        Unpacks the JavaScript code.

        :return: The unpacked JavaScript code, or None if the code couldn't be unpacked.
        """
        try:
            pattern = re.compile(r'"}\("([^"]+)",[^,]+,\s*"([^"]+)",\s*(\d+),\s*(\d+)', re.DOTALL)
            search_results = pattern.search(self.hunter_js)
            if search_results is not None and search_results.group(4) is not None:
                h = search_results.group(1)
                n = search_results.group(2)
                t = int(search_results.group(3))
                e = int(search_results.group(4))
                return self.hunter(h, n, t, e)
        except Exception as e:
            log_error(e)
        return None

    def duf(self, d: str, e: int, f: int = 10) -> int:
        """
        Decodes a string using a simple substitution cipher.

        :param d: The string to be decoded.
        :param e: The number of characters to use in the substitution cipher.
        :param f: The base to use for the substitution cipher.
        :return: The decoded string.
        """
        str_ = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
        g = list(str_)
        h = g[:e]
        i = g[:f]
        d_list = list(reversed(d))
        j = 0.0
        for c, b in enumerate(d_list):
            if b in h:
                j += h.index(b) * e**c
        k = ""
        while j > 0:
            k = i[int(j % f)] + k
            j = (j - j % f) / f
        return int(k) if k.isnumeric() else 0
    
    def hunter(self, h: str, n: str, t: int, e: int) -> str:
        """
        Unpacks the JavaScript code.

        :param h: The encoded string.
        :param n: The substitution cipher to use.
        :param t: A value to subtract from the decoded result.
        :param e: The base to use for the substitution cipher.
        :return: The unpacked JavaScript code.
        """
        result = ""
        i = 0
        while i < len(h):
            j = 0
            s = ""
            while h[i] != n[e]:
                s += h[i]
                i += 1
            while j < len(n):
                s = s.replace(n[j], j.digit_to_char())
                j += 1
            result += (self.duf(s, e) - t).to_char()
            i += 1
        return result
