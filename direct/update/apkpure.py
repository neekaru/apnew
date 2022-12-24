from cloudscraper import exceptions

from util.html.parser import get_bs4, get_link_or_title
from util.network.http import rget


def get_dl(url):
    get_info = url if "-APK" in url else f"{url}/download?from=details"
    try:
        base = get_bs4(rget(get_info, is_cf=True).text)
        return {
            "package_name": get_link_or_title(
                base, tag="a", args={"class": "info-value"}
            ),
            "Architecture": get_link_or_title(
                base,
                tag="p",
                args={"class": "info-value"},
                css="#li:nth-child(5) > div.info",
            ),
            "dl_link": get_link_or_title(
                base, attr="href", tag="a", args={"class": "ga"}
            ),
            "signature": get_link_or_title(
                base, tag="p", args={"class": "info-value"}, css="#li.sign > div.info"
            ),
        }
    except exceptions.CloudflareChallengeError as e:
        return {"msg": f"Hari ini aku sedih karena {e}"}
