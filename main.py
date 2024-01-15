from webserver import Webserver
from aiohttp import web

if __name__ == "__main__":
    server = Webserver("web/")
    web.run_app(server)
