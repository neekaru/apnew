import codecs
import re
from typing import Optional, Union
from urllib.parse import quote as quot
from urllib.parse import quote_plus as quot_plus
from urllib.parse import unquote as unquot
from urllib.parse import urlparse

from w3lib.url import url_query_cleaner


class Url:
    def __init__(self, url: str, bs4: str = None):
        self.url = url
        self.bs4 = bs4

    def cleanurl(self, *args, **kwargs):
        return url_query_cleaner(self.url, *args, **kwargs)

    def getfilehost(self, hostname: bool = False) -> str:
        parsed_url = urlparse(self.url)
        if hostname:
            return parsed_url.hostname
        else:
            return parsed_url.path.strip("/ ").split("/")[-1]

    def fix_annoy(
        self,
        double_newline: bool = False,
        double_space: bool = False,
        remove_part: Optional[str] = None,
        unicode_escape: Optional[bool] = None,
        weird_unicode_remover: Optional[bool] = None,
    ):
        if double_newline:
            bs4 = self.bs4.replace("\n", "").rstrip()
        if double_space and remove_part is None:
            bs4 = self.bs4.replace("  ", "")
        if remove_part is not None:
            bs4 = re.sub(remove_part, "", self.bs4)
            bs4 = bs4.lstrip()
        if unicode_escape is not None:
            return codecs.decode(self.bs4, "unicode_escape")
        if weird_unicode_remover is not None:
            return re.sub(r"[^\x00-\x7F]", "", self.bs4)
        return bs4

    def fix_url(
        self,
        *,
        clean: bool = False,
        quote_plus: bool = False,
        quote: bool = False,
        quote_fix: bool = False,
        unquote: bool = False,
    ) -> Union[str, None]:
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
