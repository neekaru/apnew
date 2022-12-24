import re
import secrets

import PyBypass as direk_1

from util.html.parser import (
    download_webpage,
    download_webpage_with_post,
    extract_form_data,
    fix_url,
    get_link_single,
    getfilehost,
)
from util.network.http import HEADER_DEFAULT
from util.utils import get_readable_size, uegen


def direct_link(query: str) -> dict:
    url_handlers = {
        "oxy.cloud": oxycloud,
        "eg.sharezweb.com": sharezweb,
        "sharezweb.com": sharezweb,
        "linkbox.to": sharezweb,
        "devuploads.com": devuploads().direct,
    }

    handler_func = next(
        (func for domain, func in url_handlers.items() if domain in query),
        None,
    )
    if handler_func is not None:
        return handler_func(query)
    # No matching function was found, try using direk_1.bypass()
    try:
        d1 = direk_1.bypass(query)
        if "bypassed_url" in d1:
            return {
                "status": True,
                "dl_url": fix_url(d1["bypassed_url"], quote_fix=True),
            }
    except Exception:
        return {"Status": False, "msg": "your link is unsupported"}


class devuploads:
    def __init__(self):
        self.__headers_one: dict = (
            {
                "User-Agent": uegen(default=True),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us,en;q=0.6",
                "Sec-Fetch-Mode": "navigate",
                "Referer": "https://dev.miuiflash.com/",
            },
        )
        self.__headers_two: dict = {
            "User-Agent": uegen(default=True),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.6",
            "Sec-Fetch-Mode": "navigate",
            "Referer": "https://devuploads.com/",
        }

    def selected_url(self, step: bool = False) -> str:
        links = [
            "become-android-developer-complete-roadmap",
            "why-you-should-learn-web-development",
            "why-develop-android-applications-instead-of-ios",
        ]
        if not step:
            return f"https://dev.miuiflash.com/{secrets.choice(links)}"
        selected_link = links[secrets.randbelow(len(links))]
        return f"https://dev.miuiflash.com/{selected_link}"

    def direct(self, query: str) -> str:
        dl = download_webpage(query, headers=HEADER_DEFAULT, parse_as="html")
        form_first = dl.find("form", attrs={"id": "downloadpage"})
        inputs_first = form_first.find_all("input", attrs={"type": "hidden"})
        form_data_first = {input["name"]: input["value"] for input in inputs_first}
        dl_ps = download_webpage_with_post(
            self.selected_url(step=True), headers=HEADER_DEFAULT, data=form_data_first
        )
        form_secound = dl_ps.find("form", {"name": "F1"})
        data_first = extract_form_data(form_secound)
        response = download_webpage_with_post(
            form_secound["action"], headers=self.__headers_one, data=data_first
        )
        form_third = response.find("form", {"id": "techyneed"})
        data_second = extract_form_data(form_third)

        # Call the linksucess function to generate the action URL
        action_url = self.selected_url(step=False)
        final = download_webpage_with_post(
            action_url, headers=self.__headers_two, data=data_second
        )
        dl_link = re.search(r'window\.location\s*=\s*"([^"]*)"', str(final)).group(1)
        return dl_link


def sharezweb(
    url: str,
) -> dict[str, bool | str | list[dict[str, str | int]] | dict[str, str | int]]:
    """
    Sharezweb/Linkbox Direct Generator
    By Nekaru
    Port from https://github.com/mirror/jdownloader/commit/759d7e44ae27025447e10cc7a20e2793f36321bd
    """
    if "/link" in url:
        api_link = f"https://{getfilehost(url, hostname=True)}/api/file/detail?itemId={getfilehost(url)}&needUser=1&needTpInfo=1&token="
    elif "/a/f" in url:
        decrypt_link = f"https://{getfilehost(url, hostname=True)}/api/file/share_out_list?shareToken={getfilehost(url)}&needTpInfo=1&scene=singleItem"
        get_token = download_webpage(
            decrypt_link, headers=HEADER_DEFAULT, parse_as="json"
        )["data"]["itemId"]
        api_link = f"https://{getfilehost(url, hostname=True)}/api/file/detail?itemId={get_token}&needUser=1&needTpInfo=1&token="
    # parse as normal
    dl = download_webpage(api_link, headers=HEADER_DEFAULT, parse_as="json")
    if dl["status"] == 500:
        return {"Status": False, "error": dl["msg"]}
    else:
        return sharezweb_extractor(dl)


# TODO Rename this here and in `sharezweb`
def sharezweb_extractor(dl) -> dict:
    cover = dl["data"]["itemInfo"].get("cover", "")
    name = dl["data"]["itemInfo"].get("name", "")
    utime = dl["data"]["itemInfo"].get("utime", "")
    tipe = dl["data"]["itemInfo"].get("type", "")
    sub_type = dl["data"]["itemInfo"].get("sub_type", "")
    size = dl["data"]["itemInfo"].get("size", "")
    video_link = dl["data"]["itemInfo"].get("url", "")
    avatar = dl["data"]["userInfo"].get("avatar", "")
    nickname = dl["data"]["userInfo"].get("nickname", "")

    resolution_list = dl["data"]["itemInfo"].get("resolutionList", [])
    data = []
    for resolution in resolution_list:
        reso = resolution["resolution"]
        sub_type1 = resolution["sub_type"]
        size1 = resolution["size"]
        video_link1 = resolution["url"]
        data.append(
            {
                "cover": cover,
                "name": name,
                "time": utime,
                "resolution": reso,
                "type": tipe,
                "ext": sub_type1,
                "size": get_readable_size(size1),
                "url": video_link1,
            }
        )

    return {
        "avatar": avatar,
        "nickname": nickname,
        "data": data,
        "data_orig": [
            {
                "cover": cover,
                "name": name,
                "time": utime,
                "type": tipe,
                "ext": sub_type,
                "size": get_readable_size(size),
                "url": video_link,
            }
        ],
    }


def oxycloud(query: str) -> str:  # sourcery skip: use-getitem-for-re-match-groups
    """
    Oxycloud Direct Generator
    By Nekaru
    """
    base = download_webpage(query, headers=HEADER_DEFAULT, parse_as="html")
    base1 = get_link_single(base.find("a", {"class": "btn btn-primary btn-lg"}), "href")
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "referer": query,
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "user-agent": uegen(default=True),
    }
    base2 = download_webpage(base1, headers=headers, parse_as="html")
    regex = r"page_url\s*=\s*'(.*?)';"
    if match := re.search(regex, str(base2)):
        page_url = match.group(1)
    return page_url
