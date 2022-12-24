import os
import re
import signal
import time

from flask import Flask, jsonify, render_template, request

from direct.direk import direct_link
from direct.media.music import spotify
from direct.media.stream import fb, helo, pinterest, snackvideo, tiktik, twitter
from direct.rom import coolrom
from direct.update.apkmirror import grab, home
from direct.update.apkpure import get_dl as apk_dl
from direct.update.uptodown import get_dl as upget_dl
from util.exceptions import FukUSeragent, GagalDikarenakan
from util.html.parser import cleanurl, download_webpage, get_link_or_title, getfilehost
from util.utils import fix_link

app = Flask(__name__)


@app.route("/")
def index():
    time.sleep(10)
    return render_template("index.html")


# needed since i manage some update on nvim
@app.route("/shutdown", methods=["GET"])
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
    request.args.get("url")
    return


@app.route("/berita", methods=["GET"])
def berita():
    news = request.args.get("sumber", type=str, default="")
    if not news:
        return {"msg": "masukan website berita"}
    page = request.args.get("page", type=int, default="")
    return page


@app.route("/song/<path:path1>", methods=["GET"])
def song(path1):
    if "spotify" in path1:
        if song := request.args.get("song"):
            return spotify().main(song)
        else:
            return {"Status": False, "msg": "No song specified"}


@app.route("/update", methods=["GET"])
def up():
    query = request.args.get("apps")
    if not query:
        return {"msg": "Masukan nama aplikasi"}

    try:
        if query == "whatsapp_desktop":
            return upget_dl("https://whatsapp-desktop.en.uptodown.com/windows")
        elif query == "apkpure":
            return apk_dl(query)
        elif query == "apkmirror":
            return home(query) or grab(query) or "nothing"
        else:
            raise ValueError("Invalid query")
    except Exception as e:
        return {"msg": f"aplikasi tidak tersedia {e}"}


@app.route("/ammusic", methods=["GET"])
def amazon():
    if not request.args.get("url"):
        return {"msg": "Masukan Url Anda"}
    query = request.args.get("url")
    try:
        if "amazon" in query:
            c1 = (
                cleanurl(query, ["marketplaceId", "musicTerritory", "ref"], remove=True)
                .replace("/music/player", "")
                .replace("amazon", "music.amazon")
            )
            return {"Status": True, "result": c1}
        elif "music.amazon" in query:
            c1 = cleanurl(
                query, ["marketplaceId", "musicTerritory", "ref"], remove=True
            )
            return {"Status": True, "result": c1}
    except Exception as e:
        return {"Status": False, "msg": e}


def get_domain(url):
    """Extract the domain from a URL."""
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
        "s.helo-app.com": heloo,
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
            return {
                "Status": True,
                "username": username,
                "caption": capt,
                "thumb_link": thumb,
                "video": mp4,
                "audio": mp3,
            }
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
    d2 = direct_link(query)
    try:
        return {"Status": True, "dl_url": d2}
    except Exception:
        return d2


@app.route("/rom", methods=["GET"])
def rom():
    if not request.args.get("url"):
        return

    query = request.args.get("url")
    try:
        if "coolrom.com.au" in query:
            return coolrom(query)
        elif "romsfun.com" in query:
            return

        # Check if the query is from romhustler.org or romulation.org
        if "romhustler.org" in query or "romulation.org" in query:
            links = []
            bs4 = download_webpage((query), parse_as="html")
            # to get guest token
            first_link = get_link_or_title(
                bs4, attr="href", tag="a", args={"class": "btn btn-yellow"}
            )
            data = download_webpage(
                f"https://{getfilehost(query, hostname=True)}{first_link}",
                parse_as="html",
            )
            # this need for data
            try:
                warning = [
                    ver.get_text()
                    for ver in data.select(
                        "#section > div > section:nth-child(2) > div.alert.alert-danger > ul > li"
                    )
                ][0]
                if warning is not None:
                    return {"msg": f"file error because {warning}"}
            except IndexError:
                # for get all url
                title = get_link_or_title(
                    data,
                    tag="td",
                    args={"class": "details-table"},
                    multiple=True,
                    force=True,
                )[2]
                filesize = get_link_or_title(
                    data, tag="td", args={"class": "details-table"}, force=True
                )
                links.extend(
                    link["href"]
                    for link in data.find(
                        "div", {"class": "details-container"}
                    ).find_all(href=True)
                )
                return {"dl_url": links.pop(0), "title": title, "filesize": filesize}
    except Exception as e:
        return {"status": False, "msg": str(e)}
