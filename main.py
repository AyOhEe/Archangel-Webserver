from webserver import Webserver
from aiohttp import web

import argparse
import configparser



if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.cfg")
    Webserver.prepare_configs(config)

    
    parser = argparse.ArgumentParser(
        prog='Archangel Webserver',                             
        description='Hosts a website used to communicate with the attached arduino'
    )
    args = parser.parse_args()


    server = Webserver("web/")
    web.run_app(server)
