import os
import signal
import time
import re

import PyBypass as direk_1
from flask import Flask, g, jsonify, redirect, render_template, request

from direct.media.music import soundcloud, spotify
from direct.media.stream import fb, pinterest, snackvideo, tiktik, twitter, helo
from direct.rom import coolrom
from direct.update import apkmirror
from direct.update.apkpure import get_dl as apk_dl
from direct.update.uptodown import get_dl as upget_dl
from util.exceptions import FukUSeragent, GagalDikarenakan
from util.html.parser import (cleanurl, fix_url, get_bs4, get_link_single,
                              getfilehost)
from util.network.http import rget
from util.utils import fix_link

app = Flask(__name__)
    
@app.route("/")
def index():
    time.sleep(10)
    return render_template("index.html")

# needed since i manage some update on nvim
@app.route("/shutdown", methods=['GET'])
def shutdown():
    jsonify({"Status": True, "message": "Shutting down..."})
    time.sleep(10)
    sig = getattr(signal, "SIGKILL", signal.SIGTERM)
    os.kill(os.getpid(), sig)

# as template
@app.route("/test", methods=["GET"])
def test():
    if not request.args.get("url"):
        # for testing perpouse
        # return render_template("404.html")
        return
    query = request.args.get("url")
    return

@app.route("/berita", methods=["GET"])
def berita():
    news = request.args.get("sumber", type=str, default="")
    if not news:
        return {"msg": "masukan website berita"}
    page = request.args.get("page", type=int, default="")
    return
    
@app.route("/song/<path:path1>", methods=["GET"])
def song(path1):
    if "spotify" in path1:
        try:
            song = request.args.get("song")
            return spotify().main(song)
        except:
            return {"Status": False, "msg": "kamu nanya"}

@app.route("/update", methods=["GET"])
def up():
    if not request.args.get("apps"):
        return {"msg": "Masukan nama aplikasi"}
    query = request.args.get("apps")
    # apk = request.args.get("apk")
    try:
        if "whatsapp_desktop" in query:
            return upget_dl("https://whatsapp-desktop.en.uptodown.com/windows")
        elif "apkpure" in query:
            return apk_dl(query)
        elif "apkmirror" in query:
            try:
                d = apkmirror.home(query)
                return d
            except:
                try:
                    d = apkmirror.grab(query)
                    return d
                except:
                    return "nothing"
    except Exception as e:
        return {"msg": f"aplikasi tidak tersedia {e}"}
        
@app.route("/ammusic", methods=["GET"])
def amazon():
    if not request.args.get("url"):
        return {"msg": "Masukan Url Anda"}
    query = request.args.get("url")
    try:
        if "amazon" in query:
            c1 = cleanurl(query, ['marketplaceId', 'musicTerritory', 'ref'], remove=True).replace("/music/player", '').replace('amazon', 'music.amazon')
            return {"Status": True, "result": c1}
        elif "music.amazon" in query:
            c1 = cleanurl(query, ['marketplaceId', 'musicTerritory', 'ref'], remove=True)
            return {"Status": True, "result": c1}
    except Exception as e:
        return {"Status": False, "msg": e}


def get_domain(url):
    """Extract the domain from a URL."""
    import re
    return match.group(1) if (match := re.search(r"https?://([^/]+)/?", url)) else None

@app.route("/stream", methods=["GET"])
def mediaStream():
    heloo = helo().result
    stream_handlers = {
        "pinterest.com": pinterest,
        "pin.it": pinterest,
        "twitter.com": twitter,
        "fb.watch": fb,
        "facebook.com": fb,
        "vm.tiktok.com": tiktik,
        "sck.io": snackvideo,
        "snackvideo.com": snackvideo,
        "s.helo-app.com": heloo
    }

    if not request.args.get("url"):
        return {"msg": "Masukan Url Anda"}
    query = request.args.get("url")
    domain = get_domain(query)
    try:
        stream_handler = stream_handlers[domain]
        if domain == "pin.it":
            queri = fix_link(query)
            result = stream_handler(queri)
        elif domain == "vm.tiktok.com":
            # extract the necessary fields from the result of the tiktik function
            b = stream_handler(queri)
            mp3 = b["data"]["mp3"]
            mp4 = b["data"]["mp4"]
            thumb = b["data"]["video_img"]
            capt = b["data"]["video_info"]
            username = b["data"]["nick"]
            # return the extracted fields as a dictionary
            return {"Status": True, "username": username, "caption": capt, "thumb_link": thumb, "video": mp4, "audio": mp3}
        else:
            result = stream_handler(query)
        return {"success": True, "result": result}
    except KeyError:
        return {"msg": f"Unsupported domain: {domain}"}
    except (GagalDikarenakan, FukUSeragent) as e:
        return {"msg": f"keep silent {e}"}
    except Exception as e:
        return e

@app.route("/direct", methods=["GET"])
def direct():
    if not request.args.get("url"):
        return {"msg": "Masukan Url Anda"}
    query = request.args.get("url")
    try:
        d1 = direk_1.bypass(query)
        if "bypassed_url" in d1:
            return {"Status": True, "dl_url": fix_url(d1["bypassed_url"], quote_fix=True)}
        else:
            return {"Status": True, "dl_url": d1}
    except Exception as e:
        return {"Status": False, "msg": e}


# for testing function works
@app.route("/rom", methods=["GET"])
def rom():  # sourcery skip: remove-redundant-if
    if not request.args.get("url"):
        return
    query = request.args.get("url")
    try:
        if "coolrom.com.au" in query:
            # to fix another issue url
            return coolrom(query)
        elif "romsfun.com" in query:
            return
        elif "romhustler.org" or "romulation.org" in query:
            links = []
            bs4 = get_bs4(rget(query).text)
            # to get guest token
            base = bs4.find("a", {"class": "btn btn-yellow"})
            first_link = get_link_single(base, "href")
            data = get_bs4(rget(f"https://{getfilehost(query, hostname=True)}{first_link}").text)
            # this need for data
            try:
                warning = [ver.get_text() for ver in data.select("#section > div > section:nth-child(2) > div.alert.alert-danger > ul > li")][0]
                if warning is not None:
                    return {"msg": f"file error because {warning}"}
            except:
                # for get all url
                title = data.find("table", {"class": "details-table"}).find("td").find_next("td").get_text()
                filesize = data.find("table", {"class": "details-table"}).find("td").find_next("td").find_next("td").find_next("td").get_text()
                links.extend(link["href"] for link in data.find("div", {"class": "details-container"}).find_all(href=True))
                return {"dl_url": links.pop(0), "title": title, "filesize": filesize}
    except Exception as e:
        return {"Status": False, "msg": e}
