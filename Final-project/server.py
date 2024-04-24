import http.server
import socketserver
import termcolor
import jinja2 as j
from pathlib import Path
import json



IP = "127.0.0.1"
PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

#with open('json/species_list.json', 'r') as f:
#    species_dict = json.load(f)


#print(species_dict["species"][0])

def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents



class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green',force_color=True)

        command = self.requestline.split(" ")[1].replace("/info", "").replace(".html", "")
        command2 = command.split("?")[0]

        SERVER = "rest.ensembl.org"
        PARAMS = "?content-type=application/json"

        ENDPOINT = "/info/species"
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

        response_species = json.loads(r1.read().decode("utf-8"))


        if command == "/" or command == "/index":
            contents = open("html/index.html", "r").read()
            content_type = 'text/html'
            error_code = 200


        elif command2 == "/listSpecies":

            try:
                limit = command.split("=")[1].strip()
                limit = int(limit)
            except ValueError:
                limit = ""

            species = []
            if limit != "":
                for i in range(0, limit):
                    species.append(response_species["species"][i]["display_name"])
            else:
                for e in response_species["species"]:
                    species.append(e["display_name"])

            list_species = ""
            for e in species:
                list_species += "· " + e + "<br>"

            contents = read_html_file("listSpecies.html").render(context={"todisplay": len(response_species["species"]), "todisplay2": limit, "todisplay3": list_species})
            content_type = 'text/html'
            error_code = 200


        elif command2 == "/Karyotype":
            common_name = command.split("=")[1].strip()
            common_name = common_name.replace("+", "_")

            for e in response_species["species"]:
                if e["common_name"] == common_name:
                    species_name = e["name"]


                    ENDPOINT = "/info/assembly/" + species_name
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

                    karyotype = response["karyotype"]
                    list_karyotype = ""
                    for e in karyotype:
                        list_karyotype += "· " + e + "<br>"

                    contents = read_html_file("Karyotype.html").render(context={"todisplay": list_karyotype})
                    error_code = 200
                    content_type = 'text/html'

                else:
                    contents = open("html/error.html", "r").read()
                    error_code = 200
                    content_type = 'text/html'

        elif command2 == "\chromosomeLength":

            contents = read_html_file("chromosomeLength.html").render(context={"todisplay": list_karyotype})
            content_type = 'text/html'
            error_code = 200

        else:
            contents = open("html/error.html", "r").read()
            error_code = 200
            content_type = 'text/html'

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