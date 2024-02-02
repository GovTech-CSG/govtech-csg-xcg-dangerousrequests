from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

import requests


def serve_http():
    httpd = HTTPServer(("127.0.0.1", 8001), SimpleHTTPRequestHandler)

    def serve_forever(httpd):
        with httpd:
            httpd.serve_forever()

    Thread(target=serve_forever, args=(httpd,)).start()
    return httpd


if __name__ == "__main__":
    httpd = serve_http()
    print("hello world")
    print(requests.get("http://localhost:8001").content)
    print("Shutting down httpd")
    httpd.shutdown()
