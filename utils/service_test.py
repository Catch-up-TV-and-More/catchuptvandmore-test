# This file is part of Catch-up TV & More
import argparse
import os
import pickle
import re
import ssl
import sys
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer

import requests

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

PY3 = sys.version_info >= (3, 0, 0)

CWD_PATH = os.path.dirname(os.path.abspath(__file__))


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    header_file = None

    @classmethod
    def set_header_file(cls, file):
        header_file = file

    def do_POST(self):
        """Handle http post requests, used for license"""
        path = self.path  # Path with parameters received from request e.g. "/license?id=234324"

        if '/license' not in path:
            self.send_response(404)
            self.end_headers()
            return
        try:
            length = int(self.headers.get('content-length', 0))
            isa_data = self.rfile.read(length).decode('utf-8').split('!')
            challenge = isa_data[0]
            session_id = isa_data[1]
            license_data = None
            if 'cense=' in path:
                path2 = path.split('cense=')[-1]

                with open(self.header_file, 'rb') as f1:
                    ab = pickle.load(f1)

                result = requests.post(url=path2, headers=ab, data=challenge, verify=False).text

                license_data = re.findall('ontentid=".+?">(.+?)<', result)[0]
                if PY3:
                    license_data = license_data.encode(encoding='utf-8', errors='strict')

            self.send_response(200)
            self.end_headers()
            self.wfile.write(license_data)
        except Exception:
            self.send_response(500)
            self.end_headers()


def init_test():
    parser = argparse.ArgumentParser(description="Catch-up TV & More Service tester")

    parser.add_argument(
        "-a",
        "--addon-path",
        default="",
        help="Path of plugin.video.catchuptvandmore",
    )

    _config = vars(parser.parse_args())

    if _config["addon_path"] == "":
        raise Exception("You need to specify the path of plugin.video.catchuptvandmore (see --help)")
    _config["addon_path"] = os.path.abspath(_config["addon_path"])

    header_file = os.path.join(
        _config["addon_path"],
        "..",
        "..",
        "userdata",
        "addon_data",
        "plugin.video.catchuptvandmore",
        "headersCanal"
    )

    SimpleHTTPRequestHandler.header_file = header_file

    address = '127.0.0.1'  # Localhost
    # The port in this example is fixed, DO NOT USE A FIXED PORT!
    # Other add-ons, or operating system functionality, or other software may use the same port!
    # You have to implement a way to get a random free port
    port = 5057
    server_inst = TCPServer((address, port), SimpleHTTPRequestHandler)
    # The follow line is only for test purpose, you have to implement a way to stop the http service!
    server_inst.serve_forever()


if __name__ == '__main__':
    init_test()
