import aiohttp_jinja2
import aiohttp
import asyncio
import jinja2
import os

from aiohttp import web
from arduino import Arduino
from arduino import DummyArduino




class Webserver(web.Application):
    USE_DUMMY_ARDUINO = False
    if os.name ==  "nt":
        ARDUINO_PORT = "COM1"
    else:
        ARDUINO_PORT = "/dev/ttyACM0"


    def __init__(self, templates_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        aiohttp_jinja2.setup(self, loader=jinja2.FileSystemLoader(templates_path))
        self.add_routes([
            web.get("/", self.index),
            web.get("/blinkrate_control.js", self.get_static("web/blinkrate_control.js")),

            web.get("/blinkrate_ws", self.blinkrate_ws)
        ])
        
        self.ard = self.create_arduino()

        self.on_shutdown.append(self.close_arduino)

    async def close_arduino(self, app):
        self.ard.shutdown()

    def create_arduino(self):
        if Webserver.USE_DUMMY_ARDUINO:
            return DummyArduino()
        else:
            return Arduino(Webserver.ARDUINO_PORT, 115200)

    def get_static(self, path):
        async def respond_static(request):
            return web.FileResponse(path)

        return respond_static

    async def blinkrate_ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == "close":
                    await ws.close()
                else:
                    print(msg.data)
                    self.ard.try_send_message(msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print("WS Error: " + ws.exception())

        print("ws closed")
        return ws

    async def index(self, request):
        context = {}
        response = aiohttp_jinja2.render_template("index.html",
                                                  request,
                                                  context)
        return response

if __name__ == "__main__":
    server = Webserver("../web")
    web.run_app(server)

