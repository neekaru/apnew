import cherrypy
import json


class Home(object):
    @cherrypy.expose
    def home(self):
        data = {"message": "Japip Homok"}
        response = json.dumps(data)
        return response


if __name__ == "__main__":
    cherrypy.quickstart(Home(), "/")
