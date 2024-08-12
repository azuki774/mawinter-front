#!/usr/bin/env python

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/v2/records":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = [
                {
                    "id": 2,
                    "category_id": 210,
                    "category_name": "カテゴリ2",
                    "datetime": "2019-08-26T14:15:22Z",
                    "from": "ふぉーむ２",
                    "type": "タイプ２",
                    "price": 200,
                    "memo": "メモ２"
                },
                {
                    "id": 1,
                    "category_id": 200,
                    "category_name": "カテゴリ1",
                    "datetime": "2019-08-24T14:15:22Z",
                    "from": "ふぉーむ１",
                    "type": "タイプ１",
                    "price": 1000,
                    "memo": "メモ１"
                },
            ]
            responseBody = json.dumps(response)

            self.wfile.write(responseBody.encode('utf-8'))

        if self.path == "/categories":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = [
                {
                    "category_id": 200,
                    "category_name": "家賃"
                },
                {
                    "category_id": 210,
                    "category_name": "食費"
                },
                {
                    "category_id": 220,
                    "category_name": "電気代"
                }
            ]
            responseBody = json.dumps(response)

            self.wfile.write(responseBody.encode('utf-8'))

    def do_POST(self):
        self.send_response(201)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

def import_args():
    parser = argparse.ArgumentParser("mock server start")

    parser.add_argument('--host', '-H', required=False, default='0.0.0.0')
    parser.add_argument('--port', '-P', required=False, type=int, default=8080)

    args = parser.parse_args()

    return args.host, args.port

def run(server_class=HTTPServer, handler_class=MockHandler, server_name='localhost', port=8080):

    server = server_class((server_name, port), handler_class)
    server.serve_forever()

def main():
    host, port = import_args()
    run(server_name=host, port=port)

if __name__ == '__main__':
    main()
