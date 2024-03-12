import aiohttp_jinja2
import aiohttp
import asyncio
import jinja2
import os

from aiohttp import web
from arduino import Arduino
from arduino import DummyArduino




class Webserver(web.Application):
    @classmethod
    def prepare_configs(cls, config):
        cls.USE_DUMMY_ARDUINO = config["Webserver"].getboolean("UseDummyArduino", False)
        cls.ARDUINO_PORT = config["Webserver"].get("ArduinoPort", "/dev/ttyACM0")

        if cls.USE_DUMMY_ARDUINO:
            print("Using DummyArduino class")

        print(f"Using Arduino port: {cls.ARDUINO_PORT}")


    def __init__(self, templates_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        aiohttp_jinja2.setup(self, loader=jinja2.FileSystemLoader(templates_path))
        self.add_routes([
            web.get("/", self.index),
            web.get("/servo_control.js", self.get_static("web/servo_control.js")),
            web.get("/bootstrap.css", self.get_static("web/bootstrap.css")),

            web.get("/servo_state", self.servo_state)
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

    async def servo_state(self, request):
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

