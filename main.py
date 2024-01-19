from webserver import Webserver
from aiohttp import web


Webserver.ARDUINO_PORT = "COM3"

if __name__ == "__main__":
    server = Webserver("web/")
    web.run_app(server)
