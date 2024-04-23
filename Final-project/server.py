import http.server
import socketserver
import termcolor
import jinja2 as j
from pathlib import Path
import json



IP = "127.0.0.1"
PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green',force_color=True)
        command = self.requestline.split(" ")[1].replace("/info", "").replace(".html", "")


        if command == "/" or command == "/index":
            contents = open("html/index.html", "r").read()
            content_type = 'text/html'
            error_code = 200

        elif "listSpecies" in command:
            SERVER = "rest.ensembl.org"
            ENDPOINT = "/info/species"
            PARAMS = "?content-type=application/json"
            URL = SERVER + ENDPOINT + PARAMS

            print(f"Server: {SERVER}")
            print(f"URL: {URL}")

            conn = http.client.HTTPConnection(SERVER)

            try:
                conn.request("GET", ENDPOINT + PARAMS)
            except ConnectionRefusedError:
                print("ERROR! Cannot connect to the Server")
                exit()

            r1 = conn.getresponse()
            print(f"Response received!: {r1.status} {r1.reason}\n")

            response = json.loads(r1.read().decode("utf-8"))

            print(len(response["species"]))

            try:
                int(command[12:])
                limit = command[12:]
            except ValueError:
                limit = ""

            contents = read_html_file("listSpecies.html").render(context={"todisplay": len(response), "todisplay2": limit})
            content_type = 'application/html'

            error_code = 200



        else:
            contents = open("html/error.html", "r").read()

        self.send_response(error_code)

        self.send_header('Content-Type', content_type)
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