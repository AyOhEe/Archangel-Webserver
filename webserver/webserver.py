import aiohttp_jinja2
import jinja2
import os

from aiohttp import web
from arduino import Arduino




class Webserver(web.Application):
    if os.name ==  "nt":
        ARDUINO_PORT = "COM1"
    else:
        ARDUINO_PORT = "/dev/ttyACM0"


    def __init__(self, templates_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        aiohttp_jinja2.setup(self, loader=jinja2.FileSystemLoader(templates_path))

        self.ard = Arduino(Webserver.ARDUINO_PORT, 115200)


        self.add_routes([
            web.get("/", self.index),
            web.post("/change_blink", self.change_blink)
        ])

    async def index(self, request):
        context = {}
        response = aiohttp_jinja2.render_template("index.html",
                                                  request,
                                                  context)
        return response

    async def change_blink(self, request):
        blink_rate = (await request.post())["blinkrate"]
        self.ard.try_send_message(blink_rate)
        raise web.HTTPFound("/")

if __name__ == "__main__":
    server = Webserver("../web")
    web.run_app(server)
