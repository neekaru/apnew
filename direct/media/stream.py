import re
import time
import json

from requests.utils import DEFAULT_ACCEPT_ENCODING

from util.html.parser import fix_annoy, fix_url, get_bs4, get_link_single, trailing, download_webpage, download_webpage_with_post
from util.network.cookie import fix_cookie, get_cookie
from util.network.http import HEADER_DEFAULT, req, rget, starter
from util.utils import clean_http, uegen, get_readable_size, get_readable_time

class helo:
    def __init__(self):
        self.__headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.6',
            'Cache-Control': 'max-age=0',
            "User-Agent": uegen(default=True),
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            "Upgrade-Insecure-Requests": "1"
        } 
    
    def parser_json_from_element(self, element):
        # Extract the JSON object from the script element
        json_string = element.string  # Get the contents of the Tag object as a string
        json_string = json_string.replace('<script>window.__INITIAL_STATE__=', '').replace('window.__INITIAL_STATE__=', '')
        json_string = fix_annoy(json_string, double_newline=True).replace("   ", "").replace("       ", "").replace("       ", "").replace("undefined", '""')
        return json.loads(json_string)


    def result(self, url):
        d = download_webpage(url, headers=self.__headers, parse_as="html")
        p = d.find_all("script")[5]
        # this need to extract them
        d = self.parser_json_from_element(p)
        base_video = d["ArticleDetailInfo"]["share_download_video"]["cdn_url"]
        url_list = d["ArticleDetailInfo"]["video"]["url_list"]
        wm_list = d["ArticleDetailInfo"]["share_download_video"]["url_list"]
        data = []
        data1 = []
        for url_obj in url_list:
            text = url_obj["text"]
            size = url_obj["size"]
            expired = url_obj["url_expire"]
            urls = url_obj["urls"][0]
            data.append({"text": text, "size": get_readable_size(size), "urls": urls, "expired": get_readable_time(expired, unix_epoch=True)})
        for url_wm in wm_list:
            text = url_wm["text"]
            size = url_wm["size"]
            expired = url_wm["url_expire"]
            urls = url_wm["urls"][0]
            data1.append({"text": text, "size": get_readable_size(size), "urls": urls, "expired": get_readable_time(expired, unix_epoch=True)})
        result = {"Status": True, "data": [{"base_video": base_video, "no_wm": data, "wm_data": data1}]}
        return result

def fb(url):
    starter("https://fdown.net", single=True)
    headers = {
        'User-Agent': uegen(default=True),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': DEFAULT_ACCEPT_ENCODING,
        'Origin': 'https://fdown.net',
        'Connection': 'keep-alive',
        'Referer': 'https://fdown.net/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    data = {
        'URLz': url,
    }
    bs4 = download_webpage_with_post('https://fdown.net/download.php', headers=headers, data=data)
    sd = get_link_single(bs4.select_one("#sdlink"), "href")
    hd = get_link_single(bs4.select_one("#hdlink"), "href")
    image_url = get_link_single(bs4.select_one(".lib-img-show"), "src")
    title = fix_annoy(bs4.select_one("div.lib-row:nth-child(1)").get_text(), double_newline=True)
    des = fix_annoy(bs4.select_one("div.lib-row:nth-child(2)").get_text(), double_newline=True, remove_part="Description: ")
    waktu = fix_annoy(bs4.select_one("div.lib-row:nth-child(3)").get_text(), double_newline=True, remove_part="Duration: ")
    return {"Status": True, "data": [{"title": title, "description": des, "waktu": waktu, "video_sd": sd, "video_hd": hd, "image_url": image_url}]}

def twitter(query):
    starter("https://www.expertsphp.com/twitter-video-downloader.php")
    time.sleep(5)
    headers = {
        "accept-langunge": "en-US,en;q=0.9",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "referer": "https://www.expertsphp.com/twitter-video-downloader.php",
        "origin": "https://www.expertsphp.com",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        "user-agent": uegen(default=True)
    }
    data = {
        "url": query
    }
    d = download_webpage_with_post("https://www.expertsphp.com/instagram-reels-downloader.php", headers=headers, data=data)
    caption = clean_http(d.find("p", {"class": "text-center"}).get_text(), newline=True).strip().replace('\u3000', ' ')
    link = d.select_one("#showdata > div.col-md-4.col-md-offset-4 > a.btn.btn-primary.btn-sm.btn-block").get("href")
    return {"Status": True, "tweets": caption, "link": link}
    # base_url = "https://ssstwitter.com/"
    # d = get_bs4(rget(base_url, headers=HEADER_DEFAULT).text)
    # tfinder = d.find("form", {"class": "pure-form pure-g hide-after-request"}).get("include-vals").replace(' ', '').split(',')
    # tt = trailing(tfinder[0].replace("tt:", ""), combo=True)
    # ts = tfinder[1].replace("ts:", "")
    # # so this website have something like saveform doing years ago back when saveform was a king video downloader
    # # specially for youtube
    # comb_url = query.strip("/ ").split("https://twitter.com/")[1]
    # data = {
    #     'id': query,
    #     'locale': 'en',
    #     'tt': tt,
    #     'ts': ts,
    # }
    # headers = {
    #     'accept-language': 'en-US,en;q=0.6',
    #     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #     'hx-current-url': 'https://ssstwitter.com/',
    #     'hx-request': 'true',
    #     'hx-target': 'target',
    #     'origin': 'https://ssstwitter.com',
    #     'referer': 'https://ssstwitter.com/',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'content-length': '127',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': uegen(default=True),
    # }
    # result = get_bs4(rpost(f"{base_url}{comb_url}", data=data, headers=headers).text)
    # try:
    #     img = [i.get("src") for i in result.select("#mainpicture > div > img")][0]
    #     # caption handling
    #     d1 = [i.get_text() for i in result.select("#mainpicture > div > p")][0].replace("\n", " ")
    #     d2 = re.sub(r"https?://\S+", "", d1)
    #     caption = re.sub(r'\t+', '', d2)
    #     # reso handling
    #     reso = [i.get_text().replace('\t', '').replace("Download", "").split(",") for i in result.select("#mainpicture > div > a:nth-child(n+1)")]
    #     link = [i["href"] for i in result.select("#mainpicture > div > a:nth-child(n+1)")]
    #     # a hack to fix that
    #     my_dict = {reso[i][0]: link[i] for i in range(len(reso))}
    #     if "Back to\r\nmain page" in my_dict:
    #         return {"Status": True, "result": img, "caption": caption}
    #     else:
    #         return {"Status": True, "img_link": img, "caption": caption, "result": [my_dict]}
    # except:
    #     return {"Status": False, "Msg": "Try Again"}

def instagram(query):
    d1 = rget("https://saveig.app/en/instagram-video-downloader", headers=HEADER_DEFAULT, single=True)
    d = get_bs4(d1.text)
    data = {
        "__RequestVerificationToken": d.find("input", {"name": "__RequestVerificationToken"}).get("value"),
        "q": query, 
        "t": "media"
    }
    headers = {
        "referer": "https://saveig.app/en/instagram-video-downloader",
        "cookie": fix_cookie(get_cookie(d1, match=0), default=True),
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "content-length": "248",
        "x-requested-with": "XMLHttpRequest",
        "Accept-Encoding": DEFAULT_ACCEPT_ENCODING
    }
    data = download_webpage_with_post("https://saveig.app/api/ajaxSearch", data=data, headers=headers, single=True, parse_as="json")["data"]
    bs4 = get_bs4(data)
    thumb = bs4.find("img", {"alt": "saveig"}).get("src")
    link = get_link_single(bs4.find("div", {"class":"download-items__btn"}), "href", "a")
    return {"status": True, "thumb": thumb, "dl_link": link}

def tiktik(query):
    # for think the web we visits
    base_url = "https://downloader.bot/id"
    cookiess = {"lang": "id"}
    headers_base = {
        "User-Agent": uegen(default=True, mobile=True),
        "accept-Encoding": DEFAULT_ACCEPT_ENCODING,
        "accept-language": "en-US,en;q=0.8",
        "sec-fetch-mode": "navigate",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "referer": "https://www.google.com/"
        
    }
    download_webpage(base_url, headers=headers_base, cookies=cookiess)
    # to fool the system
    headers_fool = {
        "User-Agent": uegen(default=True, mobile=True),
        "accept-Encoding": DEFAULT_ACCEPT_ENCODING,
        "accept-language": "en-US,en;q=0.8",
        "sec-fetch-mode": "navigate",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "referer": "https://downloader.bot/id"
    }
    download_webpage("https://downloader.bot/api/stats/usersdownloaded", headers=headers_fool, cookies=cookiess)
    headers_bot = {
        "User-Agent": uegen(default=True, mobile=True),
        "accept-Encoding": DEFAULT_ACCEPT_ENCODING,
        "accept-language": "en-US,en;q=0.8",
        "sec-fetch-mode": "navigate",
        "content-length": "42",
        "content-type": "application/json",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "referer": "https://downloader.bot/id"
    }
    json_req = {
        "url": query
    }
    return download_webpage_with_post("https://downloader.bot/api/tiktok/info", headers=headers_bot, json=json_req, cookies=cookiess, parse_as="json")
    
def pinterest(query):
    """
    Pinterest anu
    """
    # to trick the website to think we load the server
    starter("https://pinterestvideodownloader.io/")
    time.sleep(5)
    headers = {
        'authority': 'pinterestvideodownloader.io',
        "accept": "*/*",
        "accept-encoding": DEFAULT_ACCEPT_ENCODING,
        "accept-langunge": "en-US,en;q=0.7",
        "content-length": "263",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        "user-agent": uegen(random=True, alter=True),
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "pll_language=en",
        "referer": "https://pinterestvideodownloader.io/",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {
        'action': 'pvd_user_download_request',
        'link': query,
        'requestlink': 'https://pinterestvideodownloader.io/',
        'deftab': 'video',
    }
    response = download_webpage_with_post('https://pinterestvideodownloader.io/wp-admin/admin-ajax.php', headers=headers, data=data, single=True)
    return get_link_single(response.select_one('#pvd_preview_img'), "src")


def snackvideo(query):
    """
    SnackVideo direct video
    """
    starter("https://www.expertstool.com/snack-video-downloader/")
    time.sleep(5)
    headers = {
        "referer": "https://www.expertstool.com/snack-video-downloader/",
        "sec-fetch-site": "same-origin",
        "user-agent": uegen(default=True, alter=True),
    }
    dp = fix_url(query, quote_plus=True)
    d = rget(f"https://www.expertstool.com/d.php?url={dp}", headers=headers)
    b = get_bs4(d.text)
    link = get_link_single(b.find("source"), "src")
    return {"success": d.status_code, "vid_url": link}





