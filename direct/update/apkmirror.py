from util.html.parser import get_bs4
from util.network.http import rget


def home(url):
    """
    for grabbing home
    """
    d = get_bs4(rget(url, is_cf=True).text)
    titles = []
    links = []
    tanggals = []
    for i in d.select(
        "#primary > div.listWidget.p-relative > div:nth-child(n+2) > div.appRow > div > div:nth-child(2) > div > h5"
    ):
        title = i.get_text().replace("\n", "").rstrip()
        titles.append(title)

    for i in d.select(
        "#primary > div.listWidget.p-relative > div:nth-child(n+2) > div.appRow > div > div:nth-child(2) > div > h5 > a"
    ):
        link = i.get("href")
        links.append(link)

    for i in d.select(
        "#primary > div.listWidget.p-relative > div:nth-child(n+2) > div.appRow > div > div:nth-child(2) > span > span"
    ):
        tanggal = i.get_text()
        tanggals.append(tanggal)

    return [
        {
            "judul": title,
            "link": f"https://www.apkmirror.com{link}",
            "tanggal": tanggal,
        }
        for title, link, tanggal in zip(titles, links, tanggals)
    ]
    # d = get_bs4(rget(url, is_cf=True).text)
    # title = [i.get_text().replace('\n','').rstrip() for i in d.select("#primary > div.listWidget.p-relative > div:nth-child(2) > div.appRow > div > div:nth-child(2) > div > h5")][0]
    # link =  [i.get("href") for i in d.select("#primary > div.listWidget.p-relative > div:nth-child(2) > div.appRow > div > div:nth-child(2) > div > h5 > a")][0]
    # tanggal = [i.get_text() for i in d.select("#primary > div.listWidget.p-relative > div:nth-child(2) > div.appRow > div > div:nth-child(2) > span > span")][0]
    # return {"judul": f"{title}", "link": f"https://www.apkmirror.com{link}", "tanggal": f"{tanggal}"}


def grab(url):
    """
    for grab version
    """
    d = get_bs4(rget(url, is_cf=True).text)
    version = [
        i.get_text().replace("\n", "").rstrip()
        for i in d.select(
            "#content > div:nth-child(6) > div:nth-child(6) > div > div:nth-child(2) > div:nth-child(n+1) > a"
        )
    ][0]
    buildversion = [
        i.get_text()
        for i in d.select(
            "#content > div:nth-child(6) > div:nth-child(6) > div > div:nth-child(n+2) > div:nth-child(n+1) > span:nth-child(7)"
        )
    ]
    arch = [
        i.get_text()
        for i in d.select(
            "#content > div:nth-child(6) > div:nth-child(6) > div > div:nth-child(n+2) > div:nth-child(2)"
        )
    ]
    android = [
        i.get_text()
        for i in d.select(
            "#content > div:nth-child(6) > div:nth-child(6) > div > div:nth-child(n+2) > div:nth-child(3)"
        )
    ]
    dpi = [
        i.get_text()
        for i in d.select(
            "#content > div:nth-child(6) > div:nth-child(6) > div > div:nth-child(n+2) > div:nth-child(4)"
        )
    ]
    # for adding working link
    link = [
        i.get("href")
        for i in d.select(
            "#content > div:nth-child(6) > div:nth-child(6) > div > div:nth-child(n+2) > div:nth-child(5) > a"
        )
    ]
    link2 = [f"https://www.apkmirror.com{lenk}" for lenk in link]
    return {
        "version": version,
        "build version": buildversion,
        "arch": arch,
        "android": android,
        "dpi": dpi,
        "link": link2,
    }
