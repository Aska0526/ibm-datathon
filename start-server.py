from script.test import getSelection
from script.content import CallDash
from http.server import BaseHTTPRequestHandler, HTTPServer

class handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(20)
        if self.path.endswith(".css"):
            self.send_header('Content-type', 'text/css')
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()

        if self.path == "/":
            open_path = "/index.html"
        else:
            open_path = self.path

        with open("." + open_path, "r") as file:
            self.wfile.write(bytes(file.read(), "utf8"))
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode("ascii").split("=")[1]
        self._set_response()
        print(post_data)
        #self.wfile.write("POST request for {}".format(CallDash(post_data)).encode('utf-8'))
        CallDash(post_data)



with HTTPServer(('', 54321), handler) as server:
    server.serve_forever()