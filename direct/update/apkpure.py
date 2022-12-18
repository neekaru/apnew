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
        return {"package_name": base.select_one('body > div.main.page-q > div.left > div.box.more-info > ul > li.pkg-name-info > div.info > p.info-value > a').get_text(), "Architecture": base.select_one("body > div.main.page-q > div.left > div.box.more-info > ul > li:nth-child(5) > div.info > p.info-value").get_text(), "dl_link": base.find("a", {"class": "ga"}).get("href"), "signature": base.select_one("body > div.main.page-q > div.left > div.box.more-info > ul > li.sign > div.info > p.info-value").get_text()}
    except exceptions.CloudflareChallengeError as e:
        return {"msg": f"Hari ini aku sedih karena {e}"}