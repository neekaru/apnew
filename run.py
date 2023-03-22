from urllib.parse import urlparse

import cherrypy
from jinja2 import Environment, FileSystemLoader
from direct.file_share import File
from direct.media import Odelsi
import requests
import httpx
from handling.error import CustomException, SongInfoNotFoundError
env = Environment(loader=FileSystemLoader('templates'))

class Home(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        data = {"message": "Abcd"}
        return data

    @cherrypy.expose
    def music(self, url=None):
        rhtml = env.get_template("index.html")
        try:
            if url:
                music = Odelsi(url).result()
                d = rhtml.render(title="Demo", data=music)
            else:
                d = rhtml.render(title="Demo")
            return d
        except (requests.ConnectTimeout, httpx.ConnectTimeout):
            # handle error case here
            return cherrypy.HTTPError("500", "Backend Sedang Ada Masalah Mohon di Ulang Kembali Request nya")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def share(self, url=None):
        domain = urlparse(url).hostname
        if "mediafire.com" in domain:
            data = {"link": File(url).mediafire_result()}
        else:
            data = {"Kamu Bagus"}
        return data


if __name__ == "__main__":
    cherrypy.quickstart(Home(), "/")
