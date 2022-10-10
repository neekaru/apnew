import requests, re
from bs4 import BeautifulSoup
from ..ext import log

def matching(url):
    """ Direct generator based file-share not streaming service """
    if "mediafire.com" in url:
        return mediafire.result(url)

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
    
