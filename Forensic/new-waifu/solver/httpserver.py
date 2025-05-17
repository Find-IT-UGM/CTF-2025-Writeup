from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestLoggerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Request logged.")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        print(f"POST data: {post_data.decode('utf-8')}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Request logged.")


def run(server_class=HTTPServer, handler_class=RequestLoggerHandler, port=5000):
    server_address = ("localhost", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
