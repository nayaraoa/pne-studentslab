import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j

def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents


PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        termcolor.cprint(self.requestline, 'green', force_color=True)

        if "GET / " in self.requestline and not "msg=" in self.requestline:
            contents = open("html/form-e1.html", "r").read()
        elif "GET /echo" in self.requestline and not "msg=" in self.requestline:
            contents = open("html/form-e1.html", "r").read()
        elif "msg=" in self.requestline:
            i = self.requestline.find("=")
            name = self.requestline[i + 1:]
            name = name.replace(" HTTP/1.1", "")
            contents = read_html_file("echo.html").render(context={"todisplay": name}) # provide a dictionary to build the form
        else:
            contents = open("html/error.html", "r").read()



        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return

# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()