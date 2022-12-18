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
        based = bs.select_one("div.content > section.versions.list > div.content#versions-items-list [data-url]")
        link = based.get("data-url")
        return link
    except Exception:
        return link

def get_dl(url): 
    # first get your link
    d = check(url)
    try:
        bs = get_bs4(rget(d).text)
        dl_link = bs.select_one('#detail-download-button').get('data-url')
        size = bs.find("p", class_="size").get_text()
        version = bs.select_one('div.info > div.version').get_text()
        app_name = bs.find("h1", id="detail-app-name").get_text().replace('\n','').rstrip()
        date = bs.select_one('tr:nth-child(6) > td:nth-child(3)').get_text()

        return {
            "app_name": app_name,
            "dl_link": dl_link,
            "size": size,
            "version": version,
            "date": date,
        }
    except Exception as e:
        try:
            dl_l1 = f"{d}/download"
            response = rget(dl_l1)
            bs = get_bs4(response.text)
            # for extracting
            dl_link = bs.select_one('#detail-download-button').get('data-url')
            size = bs.find("p", class_="size").get_text()
            version = bs.select_one("div.info > div.version").get_text()
            app_name = bs.find("h1", id="detail-app-name").get_text().replace('\n','').rstrip()
            date = bs.select_one("tr:nth-child(6) > td:nth-child(3)").get_text()
            return {"app_name": app_name, "dl_link": dl_link, "size": size, "version": version, "date": date}
        except Exception as e:
            return f"HEHEHEH {e}"
            