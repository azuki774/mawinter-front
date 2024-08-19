#!/usr/bin/env python

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/v2/record":
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

        if self.path == "/v2/record/summary/2024":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = [{"category_id":100,"category_name":"月給","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":101,"category_name":"ボーナス","count":1,"price":[0,0,0,0,12231,0,0,0,0,0,0,0],"total":12231},{"category_id":110,"category_name":"雑所得","count":2,"price":[0,0,0,0,244,0,0,0,0,0,0,0],"total":244},{"category_id":200,"category_name":"家賃","count":4,"price":[0,0,0,0,490242,0,0,0,0,0,0,0],"total":490242},{"category_id":210,"category_name":"食費","count":9,"price":[0,0,0,6729,364,0,0,0,0,0,0,0],"total":7093},{"category_id":220,"category_name":"電気代","count":1,"price":[0,0,0,0,313123,0,0,0,0,0,0,0],"total":313123},{"category_id":221,"category_name":"ガス代","count":1,"price":[0,0,0,0,3313,0,0,0,0,0,0,0],"total":3313},{"category_id":222,"category_name":"水道費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":230,"category_name":"コンピュータリソース","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":231,"category_name":"通信費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":240,"category_name":"生活用品","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":250,"category_name":"娯楽費","count":1,"price":[0,0,0,0,4432,0,0,0,0,0,0,0],"total":4432},{"category_id":251,"category_name":"交遊費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":260,"category_name":"書籍・勉強","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":270,"category_name":"交通費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":280,"category_name":"衣服等費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":300,"category_name":"保険・税金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":400,"category_name":"医療・衛生","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":500,"category_name":"雑費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":600,"category_name":"家賃用貯金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":601,"category_name":"PC用貯金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":700,"category_name":"NISA入出金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":701,"category_name":"NISA変動","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0}]
            responseBody = json.dumps(response)

            self.wfile.write(responseBody.encode('utf-8'))

    def do_POST(self):
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_DELETE(self):
        self.send_response(204)
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
