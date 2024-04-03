import http.server
import socketserver
import termcolor


IP = "127.0.0.1"
PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green',force_color=True)

        if "GET / " in self.requestline:
            contents = open("html/index.html", "r").read()
        elif "/info/C" in self.requestline:
            contents = open("html/info/C.html", "r").read()
        elif "/info/A" in self.requestline:
            contents = open("html/info/A.html", "r").read()
        elif "/info/G" in self.requestline:
            contents = open("html/info/G.html", "r").read()
        elif "/info/T" in self.requestline:
            contents = open("html/info/T.html", "r").read()
        else:
            contents = open("html/error.html", "r").read()

        self.send_response(200)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))

        self.end_headers()

        self.wfile.write(contents.encode())

        return

Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()