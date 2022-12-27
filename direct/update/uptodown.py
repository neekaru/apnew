# so this common for my next feature for something like check my update bla bla
from util.html.parser import get_bs4, get_link_or_title
from util.network.http import rget


def check(url):  # sourcery skip: inline-immediately-returned-variable
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
        based = bs.select_one(
            "div.content > section.versions.list > div.content#versions-items-list [data-url]"
        )
        link = get_link_or_title(bs, css=True, selector=based, attr="data-url")
        return link
    except Exception:
        return link


def get_dl(url):
    # first get your link
    d = check(url)
    try:
        bs = get_bs4(rget(d).text)
        return func_1(bs, "div.info > div.version", "tr:nth-child(6) > td:nth-child(3)")
    except Exception:
        try:
            dl_l1 = f"{d}/download"
            response = rget(dl_l1)
            bs = get_bs4(response.text)
            return func_1(
                bs,
                "div.info > div.version",
                "tr:nth-child(6) > td:nth-child(3)",
            )
        except Exception as e:
            return f"HEHEHEH {e}"


def func_1(bs, arg1, arg2):
    """
    Just a simpler way to clean my shit code
    """
    dl_link = get_link_or_title(
        bs, attr="data-url", css=True, selector="#detail-download-button"
    )
    size = get_link_or_title(
        bs, tag="p", attr=None, **{"class_": "size"}, force_text=True
    )
    version = get_link_or_title(bs, css=True, selector=arg1)
    app_name = (
        get_link_or_title(bs, tag="h1", args={"id": "detail-app-name"}, force_text=True)
        .replace("\n", "")
        .rstrip()
    )
    date = get_link_or_title(bs, css=True, selector=arg2, attr=None)

    return {
        "app_name": app_name,
        "dl_link": dl_link,
        "size": size,
        "version": version,
        "date": date,
    }
