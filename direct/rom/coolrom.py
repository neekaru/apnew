
from util.network.http import rget
from util.html.parser import fix_url, get_bs4, get_link_single


def coolrom(query):
    qur = fix_url(query, quote_fix=True)
    bs4 = get_bs4(rget(qur).text)
    try:
        container = bs4.find('div', {'class': 'container'})
        link = get_link_single(container, "href", "a")
        return {"Status": True, "dl_url": f"https://coolrom.com.au{link}"}
    except:
        base = bs4.find("div", {"class": "modal-footer"})
        link = get_link_single(base, "href", "a")
        return {"Status": True, "dl_url": link}
