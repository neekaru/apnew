import re
import codecs
from urllib.parse import urlparse
from urllib.parse import quote as quot
from urllib.parse import quote_plus as quot_plus
from urllib.parse import unquote as unquot

from bs4 import BeautifulSoup
from w3lib.url import url_query_cleaner


class Parser_add():
    def __init__():
        return

    def cleanurl(self, url: str, *args, **kwargs):
        return url_query_cleaner(url, *args, **kwargs)

    def getfilehost(self, url: str, hostname: bool = False) -> str:
        parsed_url = urlparse(url)
        if hostname:
            return parsed_url.hostname
        else:
            return parsed_url.path.strip("/ ").split("/")[-1]

    def fix_annoy(self, bs4: str,
                  double_newline: bool = False,
                  double_space: bool = False,
                  remove_part: str | None = None,
                  unicode_escape: bool | None = None,
                  weird_unicode_remover: bool | None = None):

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

    def fix_url(self, url: str, *,
                clean: bool = False,
                quote_plus: bool = False,
                quote: bool = False,
                quote_fix: bool = False,
                unquote: bool = False,
                ) -> str | None:
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


class Parser():
    def __init__():
        return

    def get_bs4(self, url: str) -> BeautifulSoup | None:
        try:
            return BeautifulSoup(url, "html.parser")
        except Exception:
            return None
