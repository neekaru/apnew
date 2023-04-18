import json
import re
from datetime import timedelta

from handling.error import SongInfoNotFoundError
from tools.html import Parser
from tools.http import Request, Request_Add
from tools.json import decode_unicode, json_dumps_fix
from tools.url import Url

class Fix_url:
    # this need for fixing some url stuff
    def __init__(self, url: str) -> Any:
        self.url = url
        
    def odelsi_fix_url(self):
        if "spotify" in self.url:
            pattern = r"https:\/\/open\.spotify\.com\/(?:intl-id\/)?(track|album)\/([\w]+).*"
            match = re.match(pattern, self.url)
            if match:
                # change this to using format style not concat using + instead using .format()
                fixed_url = "https://open.spotify.com/{}/{}".format(match.group(1), match.group(2))
                return fixed_url
            else:
                return None
        else:
            return self.url
class Odelsi:
    def __init__(self, url):
        self.url = Fix_url(url).odelsi_fix_url()
        self._api_url_resolve = "https://api.odesli.co"
        self._base_song = "https://song.link"
        self._base_album = "https://album.link"

    # for get id for handling
    def api_check(self):
        htt = (
            Request(
                f"{self._api_url_resolve}/resolve?url={Url(self.url).fix_url(quote_plus=True)}"
            )
            .rget(
                single=True,
                timeout=15,
                headers=Request_Add.get_headers(
                    additional_headers={"Referer": "Referer: https://odesli.co/"}
                ),
            )
            .json()
        )
        return htt

    def get_html(self):
        sel = self.api_check()
        # Map provider names to URL paths
        url_paths = {
            "spotify": "/s/",
            "deezer": "/d/",
            "itunes": "/i/",
            "youtube": "/y/",
            "pandora": "/p/",
            "amazon": "/a/",
            "tidal": "/t/",
            "napster": "/n/",
            "yandex": "/ya/",
            "boomplay": "/bp/",
        }
        # Get the URL path for the current provider
        # Default to Spotify URL path
        url_path = url_paths.get(sel["provider"], "/s/")
        url_map = {
            "album": f"{self._base_album}{url_path}{sel['id']}",
            "song": f"{self._base_song}{url_path}{sel['id']}",
        }
        url = url_map.get(sel["type"])
        htt = (
            Request(url)
            .rget(
                http2=True,
                headers=Request_Add.get_headers(
                    additional_headers={"Referer": "https://odesli.co/"}
                ),
            )
            .text
        )
        pp = Parser(htt).get_bs4()
        next_data = pp.find("script", id="__NEXT_DATA__")
        js = json_dumps_fix(next_data.string, double_slash=True)
        js = json.loads(js)
        return decode_unicode(js)

    def result(self):
        d = self.get_html()
        if (
            "props" in d
            and "pageProps" in d["props"]
            and "pageData" in d["props"]["pageProps"]
        ):
            song_info = d["props"]["pageProps"]["pageData"]
            title = song_info["entityData"]["title"]
            artist = song_info["entityData"]["artistName"]
            release_date = song_info["entityData"].get("releaseDate", None)
            thumbnail_url = song_info["entityData"]["thumbnailUrl"]
            isrc = song_info["entityData"].get("isrc", None)
            duration = song_info["entityData"]["duration"]

            if release_date is None:
                formatted_release_date = None
            else:
                if song_info["entityData"]["releaseDate"]["month"] == 0:
                    song_info["entityData"]["releaseDate"]["month"] = 1
                formatted_release_date = f"{release_date['day']:02d}/{release_date['month']:02d}/{release_date['year']}"

            if duration is None:
                formatted_duration = None
            else:
                formatted_duration = str(timedelta(milliseconds=duration)).split(".")[0]

            # Extracting streaming links
            streaming_links = song_info["sections"][1]["links"]
            streaming_data = []
            for link in streaming_links:
                platform = link["platform"]
                country = link.get("country", None)
                url = link.get("url")
                display_name = link["displayName"]
                # unique_id = link.get("uniqueId")

                if country is not None and url is not None:
                    streaming_data.append(
                        {
                            "platform": platform,
                            # "country": country,
                            "url": url,
                            "display_name": display_name,
                            # "unique_id": unique_id,
                        }
                    )

            # Creating the final dictionary
            result = {
                "title": title,
                "artist": artist,
                "thumb": thumbnail_url,
                "isrc": isrc,
                "duration": formatted_duration,
                "release_date": formatted_release_date,
                "list": streaming_data,
            }
            return result
        else:
            raise SongInfoNotFoundError("song_info not found")
