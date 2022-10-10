import requests, re, math
from bs4 import BeautifulSoup
from cloudscraper import create_scraper
from api_app.ext import log

def matching(query):
    """ Direct generator based file-share not streaming service """
    if "mediafire.com" in query:
        return mediafire.result(url=query)
    elif "zippyshare.com" in query:
        return zippyshare.result(url=query)
    elif "apkadmin.com" in query or "sharemods.com" in query:
        return apkadmin.result(url=query)

class apkadmin:
    def __init__(self) -> None:
        pass
    
    def basic_data(self, op, ids):
        return {
            "op": op,
            "id": ids,
            "rand": "",
            "referer": "",
            "method_free": "",
            "method_premium": "",
        }
    
    def request(self, url: str) -> str:
        scraper = create_scraper()
        r = scraper.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        ops = soup.find("input", {"name": "op"})["value"]
        idss = soup.find("input", {"name": "id"})["value"]
        dlnk = scraper.post(url, data=apkadmin.basic_data(op=ops, ids=idss))
        dbsop = BeautifulSoup(dlnk.text, "html.parser")
        # apkadmin pattern
        try:
            link = dbsop.find("div", {"class": "text text-center"}).find("a")["href"]
        except:
            try:
                # sharemods pattern
                link = dbsop.find("a", {"id": "downloadbtn"}).get("href")
            except Exception as err:
                log.error(err)
                raise log.info(
                    "ERROR: Tidak dapat mengambil direct link"
                )
        return link
    
    def result(self, url: str):
        return {"status": True, "dl_link": apkadmin.request(url)}

class zippyshare:
    def __init__(self) -> None:
        pass

    def js_decrypt(self, base_url):
        try:
            var_a = re.findall(r"var.a.=.(\d+)", self)[0]
            mtk = int(math.pow(int(var_a), 3) + 3)
            uri1 = re.findall(r"\.href.=.\"/(.*?)/\"", self)[0]
            uri2 = re.findall(r"\+\"/(.*?)\"", self)[0]
        except:
            try:
                a, b = re.findall(r"var.[ab].=.(\d+)", self)
                mtk = eval(f"{math.floor(int(a)/3) + int(a) % int(b)}")
                uri1 = re.findall(r"\.href.=.\"/(.*?)/\"", self)[0]
                uri2 = re.findall(r"\)\+\"/(.*?)\"", self)[0]
            except:
                try:
                    mtk = eval(re.findall(r"\+\((.*?).\+", self)[0] + "+ 11")
                    uri1 = re.findall(r"\.href.=.\"/(.*?)/\"", self)[0]
                    uri2 = re.findall(r"\)\+\"/(.*?)\"", self)[0]
                except:
                    try:
                        mtk = eval(re.findall(r"\+.\((.*?)\).\+", self)[0])
                        uri1 = re.findall(r"\.href.=.\"/(.*?)/\"", self)[0]
                        uri2 = re.findall(r"\+.\"/(.*?)\"", self)[0]
                    except Exception as err:
                        log.error(err)

                return f"{base_url}/{uri1}/{int(mtk)}/{uri2}"

    def request(self) -> str:
        base_url = re.search("http.+.zippyshare.com", self).group()
        response = requests.get(self)
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
        return {"status": True, "dl_link": zippyshare.request(self=url)}

class mediafire:
    def __init__(self) -> None:
        pass

    def request(self) -> str:
        try:
            link = re.findall(r'\bhttps?://.*mediafire\.com\S+', self)[0]
            link = link.split('?dkey=')[0]
        except IndexError as e:
            raise log.error("No MediaFire links found") from e
        try:
            req = requests.get(link)
            page = BeautifulSoup(req.content, 'html.parser')
            info = page.find('a', {'aria-label': 'Download file'})
            return info.get('href')
        except Exception as e:
            log.error(e)
            raise log.info("Tidak dapat mengambil direct link") from e
        
    def result(self: str):
        return {"status": True, "dl_link": mediafire.request(self)}
    
