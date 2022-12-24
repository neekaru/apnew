from util.html.parser import fix_url, get_bs4, get_link_or_title
from util.network.http import rget


def coolrom(query):  # sourcery skip: do-not-use-bare-except
    qur = fix_url(query, quote_fix=True)
    bs4 = get_bs4(rget(qur).text)
    try:
        container = get_link_or_title(bs4, tag="div", args={"class": "container"})
        link = get_link_or_title(container, attr="href", tag="a")
        return {"Status": True, "dl_url": f"https://coolrom.com.au{link}"}
    except:
        base = get_link_or_title(bs4, tag="div", args={"class": "modal-footer"})
        link = get_link_or_title(base, attr="href", tag="a")
        return {"Status": True, "dl_url": link}
