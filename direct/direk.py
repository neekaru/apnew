import re
import random

from zippyshare_downloader import extract_info

from util.html.lib_js import jsunpack
from util.html.parser import (
    download_webpage,
    download_webpage_with_post,
    extract_data_regex,
    extract_form_data,
    extract_json_data,
    get_link_or_title,
    getfilehost,
)
from util.html.parser_new import (GetHtml, parser)
from util.network.http import HEADER_DEFAULT, get_new_headers
from util.utils import decode_string, fix_link, get_readable_size, uegen


def direct_link(query: str) -> str | dict[str, str]:
    # Define a dictionary that maps domain names to functions
    domain_to_function = {
        "hxfile.co": hxfile,
        "hexupload.net": hexupload,
        "devuploads.com": lambda query: devuploads().direct(query),
        "upstream.to": upstream,
        "uppit.com": uppit,
        "anonymfile.com": anonmyfile,
        "zippyshare.com": zippyshare,
        r"^https:\/\/www\.(eg\.sharezweb\.com|sharezweb\.com|linkbox\.to)\/.*$": sharezweb,
    }

    try:
        # Use a regular expression to match the domain name
        domain_regex = re.compile(r"|".join(domain_to_function.keys()))
        domain_match = domain_regex.search(query)
        if domain_match:
            matched_domain = domain_match.group()
            for domain in domain_to_function.keys():
                if re.match(domain, matched_domain):
                    return domain_to_function[domain](query)
            raise Exception(f"Invalid domain name encountered: {query}")

        else:
            # check for non-regex version of the domain name
            for domain in domain_to_function.keys():
                if domain in query:
                    return domain_to_function[domain](query)
            raise Exception(f"Invalid domain name encountered: {query}")
    except Exception as e:
        return {"msg": str(e)}

class devuploads:
    def __init__(self):
        pass

    def selected_url(self, step: bool = False) -> str:
        links = [
            "become-android-developer-complete-roadmap",
            "why-you-should-learn-web-development",
            "why-develop-android-applications-instead-of-ios",
            "what-is-supabase-new-tech",
            "what-is-arduino-is-it-worth",
            "a-raspberry-pi-what-is-it",
            "what-is-nim-lang-why-to-use-it",
            "remix-how-the-react-framework-competes-with-next-js",
            "what-exactly-is-next-js-and-why-do-we-use-it",
            "describe-godot-the-free-engine-for-2d-and-3d-game-development",
            "what-is-github-and-how-to-use-it",
            "what-is-blazor-for-developers",
            "what-is-sveltekit-full-guide",
            "what-does-a-developer-of-kafka-do"
        ]
        if not step:
            return f"https://dev.miuiflash.com/{random.choice(links)}"
        selected_link = links[random.randrange(len(links))]
        return f"https://dev.miuiflash.com/{selected_link}"

    def direct(self, query: str) -> str:
        # sourcery skip: inline-immediately-returned-variable, use-getitem-for-re-match-groups
        dl = GetHtml(query).download_webpage(parse_as="html", headers=HEADER_DEFAULT)
        for_m = dl.find("form")
        for_m = parser().extract_form_data(for_m)
        dl_ps = GetHtml(self.selected_url(step=True)).download_webpage_with_post(headers=HEADER_DEFAULT, data=for_m)
        # fase ke 2
        for_m_2 = dl_ps.find("form")
        for_m_2 = parser().extract_form_data(for_m_2)
        dl_ps_1 = GetHtml(dl_ps.find("form")["action"]).download_webpage_with_post(headers=HEADER_DEFAULT, data=for_m_2)
        # fase ke 3
        for_m_3 = dl_ps_1.find("form")
        for_m_3 = parser().extract_form_data(for_m_3)
        dl_ps_2 =  GetHtml(self.selected_url(step=False)).download_webpage_with_post(headers=HEADER_DEFAULT, data=for_m_3)
        final = re.search(r'window\.location\s*=\s*"([^"]*)"', str(dl_ps_2)).group(1)
        return final

def streamhide(url: str) -> str:
    """
    StreamHide Extractor Generator
    By Neekaru
    """
    d = download_webpage(url, headers=HEADER_DEFAULT)
    script = get_link_or_title(d, tag="script", raw=True, multiple=True)[19]
    pattern = re.compile(r'file:\s*"([^"]+)"')
    if match := pattern.search(script):
        # Extract the value of the "file" attribute
        file_url = match.group(1)
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
    dl_link_1 = get_link_or_title(test_post, css=".btn.btn-dow", raw=True)
    dl_link = extract_data_regex(dl_link_1, preset="a_href", group=1)
    return dl_link

def uppit(url: str) -> str:
    """
    Just Uppit
    """
    ds = download_webpage(url, headers=HEADER_DEFAULT)
    data = get_link_or_title(ds, tag="form")
    d = download_webpage_with_post(url, headers=HEADER_DEFAULT, data=data)
    return get_link_or_title(d, tag="a", attr="href", multiple=True)[4].replace(
        " ", "%20"
    )


def zippyshare(url: str) -> str:
    """
    Just zippyshare test
    """
    if "/d" in url:
        url = fix_link(url)
        return extract_info(url, download=False).download_url
    else:
        return extract_info(url, download=False).download_url


def fembed(url: str) -> dict:  # sourcery skip: use-getitem-for-re-match-groups
    url = url.replace("/v/", "/f/")
    domain = getfilehost(url, hostname=True)
    down = download_webpage(url, headers=HEADER_DEFAULT, parse_as="html")
    api_link = re.search(r"(/api/source/[^\"']+)", str(down)).group(1)
    return download_webpage_with_post(
        f"https://{domain}{api_link}",
        headers=get_new_headers(additional_headers={"Referer": url}),
        data={"r": url, "d": domain},
        parse_as="json",
    )["data"]


def anonmyfile(url: str) -> str:
    """
    Anonmyfile
    Regex from https://github.com/Gujal00/ResolveURL/commit/8c37ebe1d7714a74b2308e9c5b9f9349a4da5358
    """
    fs = download_webpage(url, headers=HEADER_DEFAULT)
    return re.search('#download.+?href="(?P<url>[^"]+)', str(fs)).group(1)

def upstream(
    url: str,
) -> str:  # sourcery skip: use-fstring-for-concatenation, use-getitem-for-re-match-groups
    """
    Upstream Direct Generator
    By Nekaru
    """
    d = download_webpage(url, headers=HEADER_DEFAULT, parse_as="html")
    script = get_link_or_title(d, tag="script", raw=True, multiple=True)[17]
    # # since the web using packerjs
    result = jsunpack.unpack(str(script))
    pattern = re.compile(r'file:\s*"([^"]+)"')
    if match := pattern.search(result):
        # Extract the value of the "file" attribute
        file_url = match.group(1)

        # Check if the URL starts with "https://s97.upstreamcdn.co"
        if not file_url.startswith("https://s97.upstreamcdn.co"):
            # Prepend "https://s97.upstreamcdn.co" to the URL
            file_url = "https://s97.upstreamcdn.co" + file_url
        return file_url


def hexupload(
    url: str,
):  # sourcery skip: use-getitem-for-re-match-groups, use-named-expression
    # HexUpload Direct Generator
    # Ported By Neekaru
    # rework from this https://github.com/Gujal00/ResolveURL/commit/e019b1fa7c27e64e801ccd9aa560235caa0cde29
    try:
        d = download_webpage(url, headers=HEADER_DEFAULT, parse_as="html")
        b4buy = re.search(r'b4aa\.buy\("([^"]+)', str(d))
        if b4buy:
            return decode_string(b4buy.group(1), "base64").replace(" ", "%20")
    except:
        pass

    try:
        payload = get_link_or_title(d, tag="form", raw=True)
        payload.update({"dataType": "json", "ajax": "1"})
        pos = download_webpage_with_post(
            "https://hexupload.net",
            data=payload,
            headers=HEADER_DEFAULT,
            response_option="headers",
        )
        js = download_webpage_with_post(
            "https://hexupload.net",
            data=payload,
            headers=HEADER_DEFAULT,
            parse_as="json",
        )
        if "text/html" not in pos["Content-Type"]:
            url = js["link"]
            if url:
                url = decode_string(url, "base64")
                return url.replace(" ", "%20")
    except:
        pass

    try:
        # for some part
        payload = {
            "op": "download2",
            "id": getfilehost(url, hostname=False),
            "rand": "",
            "referer": url,
            "method_free": "Free Download",
        }
        html = download_webpage_with_post(
            url, form_data=payload, headers=HEADER_DEFAULT, parse_as="html"
        )
        url_match = re.search(r"ldl\.ld\('([^']+)", str(html))
        if url_match:
            url = url_match.group(1)
            url = decode_string(url, "base64")
            return url.replace(" ", "%20")
    except:
        pass

    d = download_webpage(url, headers=HEADER_DEFAULT)
    # get the form
    search_form = d.find("form", {"name": "F1"})
    data = extract_form_data(search_form)
    test_post = download_webpage_with_post(
        url, headers=get_new_headers({"Referer": url}), data=data
    )
    dl_link_1 = get_link_or_title(test_post, css=".btn.btn-dow", raw=True)
    return extract_data_regex(dl_link_1, preset="a_href", group=1)


def sharezweb(
    url: str,
) -> dict[str, bool | str | list[dict[str, str | int]] | dict[str, str | int]]:
    """
    Sharezweb/Linkbox Direct Generator
    By Nekaru
    Port from https://github.com/mirror/jdownloader/commit/759d7e44ae27025447e10cc7a20e2793f36321bd
    """
    if "/link" in url:
        api_link = f"https://{getfilehost(url, hostname=True)}/api/file/detail?itemId={getfilehost(url, hostname=False)}&needUser=1&needTpInfo=1&token=&lan=en"
    elif "/a/f" in url:
        # old decrypt link
        #decrypt_link = f"https://{getfilehost(url, hostname=True)}/api/file/share_out_list?shareToken={getfilehost(url, hostname=False)}&needTpInfo=1&scene=singleItem"
        decrypt_link = f"https://{getfilehost(url, hostname=True)}/api/file/share_out_list/?sortField=utime&sortAsc=0&pageNo=1&pageSize=100&shareToken={getfilehost(url, hostname=False)}&scene=singleItem&needTpInfo=1&token=&lan=en"
        get_token = download_webpage(
            decrypt_link, headers=HEADER_DEFAULT, parse_as="json"
        )["data"]["itemId"]
        api_link = f"https://{getfilehost(url, hostname=True)}/api/file/detail?itemId={get_token}&needUser=1&needTpInfo=1&token=&lan=en"
    # parse as normal
    dl = download_webpage(api_link, headers=HEADER_DEFAULT, parse_as="json")
    if dl["status"] == 500:
        return {"Status": False, "error": dl["msg"]}
    else:
        keys = ["cover", "name", "utime", "type", "sub_type", "size", "url"]
        item_info = extract_json_data(dl["data"]["itemInfo"], keys)

        keys = ["avatar", "nickname"]
        user_info = extract_json_data(dl["data"]["userInfo"], keys)

        resolution_list = dl["data"]["itemInfo"].get("resolutionList", [])
        data = []
        for resolution in resolution_list:
            reso = resolution["resolution"]
            sub_type1 = resolution["sub_type"]
            size1 = resolution["size"]
            video_link1 = resolution["url"]
            data.append(
                {
                    "cover": item_info["cover"],
                    "name": item_info["name"],
                    "time": item_info["utime"],
                    "resolution": reso,
                    "type": item_info["type"],
                    "ext": sub_type1,
                    "size": get_readable_size(size1),
                    "url": video_link1,
                }
            )

        return {
            "avatar": user_info["avatar"],
            "nickname": user_info["nickname"],
            "data": data,
            "data_orig": [
                {
                    "cover": item_info["cover"],
                    "name": item_info["name"],
                    "time": item_info["utime"],
                    "type": item_info["type"],
                    "ext": item_info["sub_type"],
                    "size": get_readable_size(item_info["size"]),
                    "url": item_info["url"],
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
