
from util.network.http import rget
from util.html.parser import fix_url, get_bs4, get_link_single


def coolrom(query):
    qur = fix_url(query, quote_fix=True)
    bs4 = get_bs4(rget(qur).text)
    try:
        return {"Status": True, "dl_url": f"https://coolrom.com.au{get_link_single(bs4.find('div', {'class': 'container'}), a_style=True)}"}
    except:
        base = bs4.find("div", {"class": "modal-footer"})
        get_url = get_link_single(base, a_style=True)
        return {"Status": True, "dl_url": get_url}