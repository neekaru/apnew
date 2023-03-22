import cherrypy


# this only for testing only
class TestException(Exception):
    pass

class SongInfoNotFoundError(Exception):
    pass

class CustomException(Exception):
    def __init__(self, title, message, show_html=False):
        self.title = title
        self.message = message
        self.show_html = show_html

    def __str__(self):
        return f"{self.title}: {self.message}"


def handle_error():
    cherrypy.response.status = 500
    exception = cherrypy._cperror._exc_info()[1]
    cherrypy.log(str(exception), traceback=True)
    if isinstance(exception, CustomException) and exception.show_html:
        return f"<h1>{exception.title}</h1> <p>{exception.message}</p>"
