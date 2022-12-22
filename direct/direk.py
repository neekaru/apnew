from util.html.parser import download_webpage, fix_url, get_link_single, getfilehost
from util.network.http import HEADER_DEFAULT
from util.utils import uegen, get_readable_size
import re
import PyBypass as direk_1
from typing import Dict, Union, List

def direct_link(query):
    if "oxy.cloud" in query:
        return oxycloud(query)
    elif "eg.sharezweb.com" in query or "sharezweb.com" in query or "linkbox.to" in query:
        return sharezweb(query)
    else:
        try:
            d1 = direk_1.bypass(query)
            if "bypassed_url" in d1:
                return {"status": True, "dl_url": fix_url(d1["bypassed_url"], quote_fix=True)}
        except Exception:
            return {"Status": False, "msg": "your link is unsupported"}
    

def sharezweb(url: str) -> Dict[str, Union[bool, str, List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]]:
    """
    Sharezweb/Linkbox Direct Generator
    By Nekaru
    Port from https://github.com/mirror/jdownloader/commit/759d7e44ae27025447e10cc7a20e2793f36321bd
    """
    if "/link" in url:
        api_link = f"https://{getfilehost(url, hostname=True)}/api/file/detail?itemId={getfilehost(url)}&needUser=1&needTpInfo=1&token="
    elif "/a/f" in url:
        decrypt_link = f"https://{getfilehost(url, hostname=True)}/api/file/share_out_list?shareToken={getfilehost(url)}&needTpInfo=1&scene=singleItem"
        get_token = download_webpage(decrypt_link, headers=HEADER_DEFAULT, parse_as="json")["data"]["itemId"]
        api_link = f"https://{getfilehost(url, hostname=True)}/api/file/detail?itemId={get_token}&needUser=1&needTpInfo=1&token="
    # parse as normal
    dl = download_webpage(api_link, headers=HEADER_DEFAULT, parse_as="json")
    if dl["status"] == 500:
        result = {"Status": False, "error": dl["msg"]}
    else:
        cover = dl["data"]["itemInfo"].get("cover", "")
        name = dl["data"]["itemInfo"].get("name", "")
        utime = dl["data"]["itemInfo"].get("utime", "")
        tipe = dl["data"]["itemInfo"].get("type" , "")
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
            data.append({"cover": cover, "name": name, "time": utime, "resolution": reso, "type": tipe, "ext": sub_type1, "size": get_readable_size(size1), "url": video_link1})

        result = {"avatar": avatar, "nickname": nickname, "data": data, "data_orig": [{"cover": cover, "name": name, "time": utime, "type": tipe, "ext": sub_type, "size": get_readable_size(size), "url": video_link}]}
    return result

def oxycloud(query: str) -> str:  # sourcery skip: use-getitem-for-re-match-groups
    """
    Oxycloud Direct Generator
    By Nekaru 
    """
    base = download_webpage(query, headers=HEADER_DEFAULT, parse_as="html")
    base1 = get_link_single(base.find("a", {"class": "btn btn-primary btn-lg"}), "href")
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'referer': query,
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'user-agent': uegen(default=True)
    }
    base2 = download_webpage(base1, headers=headers, parse_as="html")
    regex = r"page_url\s*=\s*'(.*?)';"
    if match := re.search(regex, str(base2)):
        page_url = match.group(1)
    return page_url