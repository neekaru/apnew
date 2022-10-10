import requests, re, math
from bs4 import BeautifulSoup
from ..ext import log

def matching(url):
    """ Direct generator based file-share not streaming service """
    if "mediafire.com" in url:
        return mediafire.result(url)
    elif "zippyshare.com" in url:
        return zippyshare.result(url)

class zippyshare:
    def __init__(self) -> None:
        pass

    def js_decrypt(self, js_script: str, base_url):
        try:
            var_a = re.findall(r"var.a.=.(\d+)", js_script)[0]
            mtk = int(math.pow(int(var_a), 3) + 3)
            uri1 = re.findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
            uri2 = re.findall(r"\+\"/(.*?)\"", js_script)[0]
        except:
            try:
                a, b = re.findall(r"var.[ab].=.(\d+)", js_script)
                mtk = eval(f"{math.floor(int(a)/3) + int(a) % int(b)}")
                uri1 = re.findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
                uri2 = re.findall(r"\)\+\"/(.*?)\"", js_script)[0]
            except:
                try:
                    mtk = eval(re.findall(r"\+\((.*?).\+", js_script)[0] + "+ 11")
                    uri1 = re.findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
                    uri2 = re.findall(r"\)\+\"/(.*?)\"", js_script)[0]
                except:
                    try:
                        mtk = eval(re.findall(r"\+.\((.*?)\).\+", js_script)[0])
                        uri1 = re.findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
                        uri2 = re.findall(r"\+.\"/(.*?)\"", js_script)[0]
                    except Exception as err:
                        log.error(err)
                
                return f"{base_url}/{uri1}/{int(mtk)}/{uri2}"

    def request(self, url: str) -> str:
        base_url = re.search("http.+.zippyshare.com", url).group()
        response = requests.get(url)
        pages = BeautifulSoup(response.text, "html.parser")
        js_script = pages.find(
            "div",
            style="margin-left: 24px; margin-top: 20px; text-align: center; width: 303px; height: 105px;",
        )
        if js_script is None:
            js_script = pages.find(
                "div",
                style="margin-left: -22px; margin-top: -5px; text-align: center;width: 303px;",
            )
        js_script = zippyshare.js_decrypt(js_script, base_url=base_url)
    
    def result(self, url: str):
        return {"status": True, "dl_link": zippyshare.request(url)}

class mediafire:
    def __init__(self) -> None:
        pass

    def request(self, url: str) -> str:
        try:
            link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
            link = link.split('?dkey=')[0]
        except IndexError as e:
            raise log.error("No MediaFire links found") from e
        try:
            req = requests.get(link)
            page = BeautifulSoup(req.content, 'lxml')
            info = page.find('a', {'aria-label': 'Download file'})
            return info.get('href')
        except Exception as e:
            log.error(e)
            raise log.info("Tidak dapat mengambil direct link") from e
        
    def result(self, url: str):
        return {"status": True, "dl_link": mediafire.request(url)}
    
