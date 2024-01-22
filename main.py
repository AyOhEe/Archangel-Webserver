from webserver import Webserver
from aiohttp import web

import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Archangel Webserver',                             
        description='Hosts a website used to communicate with the attached arduino'
    )
    parser.add_argument("-d", "--usedummy", action='store_true')
    parser.add_argument("-p", "--port", default=None)
    args = parser.parse_args()

    if args.usedummy:   
        print("Using DummyArduino class")
        Webserver.USE_DUMMY_ARDUINO = True

    if args.port:
        print(f"Using Arduino port: {args.port}")
        Webserver.ARDUINO_PORT = args.port


    server = Webserver("web/")
    web.run_app(server)
