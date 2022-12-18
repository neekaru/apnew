# so this common for my next feature for something like check my update bla bla           
from util.network.http import rget
from util.html.parser import get_bs4


def check(url):
    """This need for checking latest one update

    Args:
        url (string): a kinda url

    Returns:
        any: a link for kinda what
    """
    url1 = f"{url}/versions"
    try:
        get = rget(url1)
        bs = get_bs4(get.text)
        based = bs.find("div", attrs={"class": "content"}).find("section", {"class": "versions list"}).find("div", class_="content", id="versions-items-list").select_one("[data-url]")
        link = based.get("data-url")
        return link
    except Exception:
        return link

def get_dl(url): 
    # first get your link
    d = check(url)
    try:
        bs = get_bs4(rget(d).text)
        dl_link = [dl.get("data-url") for dl in bs.select("#detail-download-button")][0] 
        size = bs.find("p", class_="size").get_text()
        version = [ver.get_text() for ver in bs.select("div.info > div.version")][0]
        app_name = bs.find("h1", id="detail-app-name").get_text().replace('\n','').rstrip()
        date = [dte.get_text() for dte in bs.select("tr:nth-child(6) > td:nth-child(3)")][0]
        return {"app_name": app_name, "dl_link": dl_link, "size": size, "version": version, "date": date}
    except Exception:
        try:
            dl_l1 = f"{d}/download"
            bs = get_bs4(rget(dl_l1).text)
            # for extracting
            # dl_link = bs.find("div", class_="button-group").find("button").get("data-url")
            dl_link = [dl.get("data-url") for dl in bs.select("#detail-download-button")][0] 
            size = bs.find("p", class_="size").get_text()
            version = [ver.get_text() for ver in bs.select("div.info > div.version")][0]
            app_name = bs.find("h1", id="detail-app-name").get_text().replace('\n','').rstrip()
            date = [dte.get_text() for dte in bs.select("tr:nth-child(6) > td:nth-child(3)")][0]
            return {"app_name": app_name, "dl_link": dl_link, "size": size, "version": version, "date": date}
        except Exception as e:
            return f"HEHEH {e}"