from cloudscraper import exceptions
from util.network.http import rget
from util.html.parser import get_bs4


def get_dl(url):
    if "-APK" in url:
        get_info = url
    else:
        get_info = f"{url}/download?from=details"
    try:
        base = get_bs4(rget(get_info, is_cf=True).text)
        return {"package_name": [dte.get_text() for dte in base.select("body > div.main.page-q > div.left > div.box.more-info > ul > li.pkg-name-info > div.info > p.info-value > a")][0], "Architecture": [dte.get_text() for dte in base.select("body > div.main.page-q > div.left > div.box.more-info > ul > li:nth-child(5) > div.info > p.info-value")][0], "dl_link": base.find("a", {"class": "ga"}).get("href"), "signature": [sig.get_text() for sig in base.select("body > div.main.page-q > div.left > div.box.more-info > ul > li.sign > div.info > p.info-value")][0]}
    except exceptions.CloudflareChallengeError as e:
        return {"msg": f"Hari ini aku sedih karena {e}"}