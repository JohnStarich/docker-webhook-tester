#!/usr/bin/env python
# Based on https://gist.github.com/bradmontgomery/2219997

from __future__ import print_function
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ssl


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        length = int(self.headers['content-length'])
        lines = self.rfile.read(length)
        print(lines)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=80,
                        help='Port to listen on')
    parser.add_argument('-s', '--ssl', action='store_true',
                        help='Enable https')
    parser.add_argument('-k', '--key-file',
                        help='Set the key file to use for server identity')
    parser.add_argument('-c', '--cert-file',
                        help='Set the cert file to use for server identity')

    args = parser.parse_args()
    server_address = ('', args.port)
    httpd = HTTPServer(server_address, Server)
    if args.ssl is True:
        httpd.socket = ssl.wrap_socket(
            httpd.socket,
            certfile=args.cert_file,
            keyfile=args.key_file,
            server_side=(args.cert_file is not None),
        )
    elif args.cert_file is not None or args.key_file is not None:
        raise Exception('Certificates or keys were specified, '
                        'but ssl not enabled')
    print('Starting server (port={port}, ssl={ssl})'.format(
        port=args.port,
        ssl=args.ssl,
    ))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
