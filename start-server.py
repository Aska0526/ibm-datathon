from script.test import getSelection
from script.content import CallDash
from http.server import BaseHTTPRequestHandler, HTTPServer
import multiprocessing 

def process1(post_data):
    CallDash(post_data)


class handler(BaseHTTPRequestHandler):
    p1 = multiprocessing.Process()
    
    def __del__(self):
        self._killDash(True)
    
    def _killDash(self, do_wait: bool):
        if handler.p1.is_alive():
            if do_wait:
                handler.p1.join()
            handler.p1.kill()
            #handler.p1.close()
   
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
        post_data = post_data.replace('+',' ')
        self._set_response()
        print(post_data)
        #self.wfile.write("POST request for {}".format(CallDash(post_data)).encode('utf-8'))

        self._killDash(False)
        handler.p1 = multiprocessing.Process(target = process1, args = [post_data],daemon=True)
        handler.p1.start()

if __name__ == "__main__":
    with HTTPServer(('', 54321), handler) as server:
        server.serve_forever()
    
