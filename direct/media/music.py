import re, json, time

from requests.utils import DEFAULT_ACCEPT_ENCODING
from util.utils import uegen
from util.network.http import rget, starter, rpost
from util.html.parser import cleanurl, get_bs4

class spotify:
    def __init__(self):
        self.__api_link = "api.spotifydown.com"
        self.__headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.8',
            'origin': 'https://spotifydown.com',
            'referer': 'https://spotifydown.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'content-encoding': DEFAULT_ACCEPT_ENCODING,
            'user-agent': uegen(default=True)
        }
    
    def song_queri(self, query):
        #clean the useless parameter
        url = cleanurl(query, ['si'], remove=True)
        return url.strip("/ ").split("/")[4]
    
    def check(self, query):  # sourcery skip: use-getitem-for-re-match-groups
        d = re.search("album|track|playlist", query)
        return d.group(0)
    
    def down(self, queri):
        down = rget(f"https://{self.__api_link}/download/{self.song_queri(queri)}", headers=self.__headers).json()
        if "track" in self.check(queri):
            artis = down["metadata"]["artists"]
            title = down["metadata"]["title"]
            link = down["link"]
            return {"artist": artis, "title": title, "dl_link": link}
        else:
            link = down["link"]
            return {"dl_link": link}
    
    def metadata(self, queri):
        mta = rget(f"https://{self.__api_link}/metadata/{self.check(queri)}/{self.song_queri(queri)}", headers=self.__headers).json()
        if "album" in self.check(queri) or "playlist" in self.check(queri):
            artis = mta["artists"]
            title = mta["title"]
            cover = mta["cover"]
            return {"title": title, "artist": artis, "cover": cover}
        elif "track" in self.check(queri):
            cover = mta["cover"]
            isrc = mta["isrc"]
            return {"cover": cover, "isrc": isrc}
    
    def tracklist(self, queri):
        trcklist = rget(f"https://{self.__api_link}/trackList/{self.check(queri)}/{self.song_queri(queri)}", headers=self.__headers)
        meh = json.loads(trcklist.text)
        meh = meh['trackList']
        if 'cover' in meh and meh['cover'] in (None, ''):
            meh.pop('cover')
        return meh
    
    def main(self, queri):
        if "track" in self.check(queri):
            meta = self.metadata(queri)
            down = self.down(queri)
            return {"metadata": [down], "adds_metadata": [meta]}
        elif "album" or "playlist" in self.check(queri):
            meta = self.metadata(queri)
            trck = self.tracklist(queri)
            return {"metadata": meta, "tracklist": trck}
        
class soundcloud:
    
    def __init__(self):
        self.__api_url = "https://www.forhub.io/download.php"
        self.__url = "https://www.forhub.io/"
        self.__headers = {
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'origin': 'https://www.forhub.io',
            'referer': 'https://www.forhub.io/soundcloud/en',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': uegen(default=True)
        }
        
    def request(self, queri):
        starter(self.__url)
        time.sleep(3)
        data = {
            "formurl": queri
        }
        return get_bs4(rpost(self.__api_url, data=data, headers=self.__headers).text)
        
    def result(self, queri):
        resul = self.request(queri)
        art = resul.find("img").get("src")
        sop = resul.prettify()
        regex = re.compile(r"onclick=\"downloadFile\('([^']+)'")
        song_link = regex.findall(sop)[0]
        return {"Status": True, "artcover": art, "song_dl": song_link}