import re
import secrets

import PyBypass as direk_1
from util.html.lib_js import jsunpack

from util.html.parser import (
    download_webpage,
    download_webpage_with_post,
    extract_form_data,
    fix_url,
    get_link_or_title,
    getfilehost,
)
from util.network.http import HEADER_DEFAULT, get_new_headers
from util.utils import get_readable_size, uegen

def direct_link(query: str) -> dict:
    # Define a dictionary that maps domain names to functions
    url_handlers = {
        "oxy.cloud": oxycloud,
        "hxfile.co": hxfile,
        "devuploads.com": devuploads().direct,
        "upstream.to": upstream
    }

    # Define a list of regular expressions and corresponding handler functions
    regex_handlers = [
        # s(re.compile(r"stapadblockuser\.xyz|streamtape\.com|streamtape\.to|streamtape\.xyz"), streamtape),
        (re.compile(r"eg\.sharezweb\.com|sharezweb\.com|linkbox\.to"), sharezweb),
    ]

    # Try to find a function in the url_handlers dictionary that matches the query
    handler_func = url_handlers.get(query)
    if handler_func is not None:
        # A matching function was found, call it and return the result
        try:
            return handler_func(query)
        except Exception as e:
            return {
                "status": False,
                "msg": f"An error occurred while calling {handler_func.__name__}: {e}",
            }

    # If no match was found in the url_handlers dictionary, try the regex_handlers list
    for pattern, handler_func in regex_handlers:
        if pattern.search(query):
            # A matching function was found, call it and return the result
            try:
                return handler_func(query)
            except Exception as e:
                return {
                    "status": False,
                    "msg": f"An error occurred while calling {handler_func.__name__}: {e}",
                }

    # If no match was found in either the url_handlers dictionary or the regex_handlers list,
    # try using direk_1.bypass()
    try:
        d1 = direk_1.bypass(query)
        if "bypassed_url" in d1:
            return {
                "status": True,
                "dl_url": fix_url(d1["bypassed_url"], quote_fix=True),
            }
        else:
            return {
                "status": False,
                "msg": "direk_1.bypass did not return a dictionary with a 'bypassed_url' key",
            }
    except Exception as e:
        return {
            "status": False,
            "msg": f"An error occurred while calling direk_1.bypass: {e}",
        }


class devuploads:
    def __init__(self):
        pass

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
        # sourcery skip: inline-immediately-returned-variable, use-getitem-for-re-match-groups
        dl = download_webpage(query, headers=HEADER_DEFAULT, parse_as="html")
        form_first = get_link_or_title(dl, tag="form", args={"id": "downloadpage"})
        inputs_first = get_link_or_title(
            form_first, tag="input", args={"type": "hidden"}, multiple=True, raw=True
        )
        form_data_first = {input["name"]: input["value"] for input in inputs_first}
        dl_ps = download_webpage_with_post(
            self.selected_url(step=True), headers=HEADER_DEFAULT, data=form_data_first
        )
        form_secound = get_link_or_title(dl_ps, tag="form", args={"name": "F1"})
        data_first = form_secound.values()
        response = download_webpage_with_post(
            form_secound["action"],
            headers=get_new_headers({"Referer": "https://dev.miuiflash.com/"}),
            data=data_first,
        )
        form_third = get_link_or_title(response, tag="form", args={"id": "techyneed"})
        data_second = form_third.values()

        # Call the linksucess function to generate the action URL
        action_url = self.selected_url(step=False)
        final = download_webpage_with_post(
            action_url,
            headers=get_new_headers({"Referer": "https://devuploads.com/"}),
            data=data_second,
        )
        dl_link = re.search(r'window\.location\s*=\s*"([^"]*)"', str(final)).group(1)
        return dl_link

def upstream(url: str) -> str:
    """
    Upstream Direct Generator
    By Nekaru
    """
    d = download_webpage(url, headers=HEADER_DEFAULT, parse_as="html")
    script = get_link_or_title(d, tag="script", raw=True, multiple=True)[17]
    # # since the web using packerjs
    result = jsunpack.unpack(str(script))
    pattern = re.compile(r'file:\s*"([^"]+)"')
    match = pattern.search(result)

    if match:
        # Extract the value of the "file" attribute
        file_url = match.group(1)

        # Check if the URL starts with "https://s97.upstreamcdn.co"
        if not file_url.startswith('https://s97.upstreamcdn.co'):
            # Prepend "https://s97.upstreamcdn.co" to the URL
            file_url = 'https://s97.upstreamcdn.co' + file_url
        return file_url

def hxfile(url: str) -> str:
    """
    Hxfile Direct Generator
    Rewrite By Nekaru From PyBypasser and lk21
    """
    d = download_webpage(url, headers=HEADER_DEFAULT)
    # get the form
    search_form = d.find("form", {"name": "F1"})
    data = extract_form_data(search_form)
    test_post = download_webpage_with_post(
        url, headers=get_new_headers({"Referer": url}), data=data
    )
    dl_link = get_link_or_title(
        test_post, tag="a", attr="href", args={"class": "btn btn-dow"}
    )
    return fix_url(dl_link, quote_fix=True)


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
    base1 = get_link_or_title(
        base, tag="a", args={"class": "btn btn-primary btn-lg"}, attr="href"
    )
    headers = get_new_headers(
        additional_headers={
            "referer": query,
            "sec-fetch-dest": "document",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
        },
        edit_headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": uegen(default=True),
        },
    )
    base2 = download_webpage(base1, headers=headers, parse_as="html")
    regex = r"page_url\s*=\s*'(.*?)';"
    if match := re.search(regex, str(base2)):
        page_url = match.group(1)
    return page_url
