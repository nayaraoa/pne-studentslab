import http.server
import socketserver
import termcolor
import jinja2 as j
from pathlib import Path
import json
from pprint import pprint
from Seq1 import Seq

IP = "127.0.0.1"
PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents

def specie_exist(list_species, name_specie):
    if name_specie in list_species:
        return True

class ServerFormat():
    def __init__(self, ENDPOINT):
        self.ENDPOINT = ENDPOINT

    def get_response(self):
        SERVER = "rest.ensembl.org"
        PARAMS = "?content-type=application/json"
        URL = SERVER + self.ENDPOINT + PARAMS

        print(f"Server: {SERVER}")
        print(f"URL: {URL}")

        conn = http.client.HTTPConnection(SERVER)

        try:
            conn.request("GET", self.ENDPOINT + PARAMS)
        except ConnectionRefusedError:
            print("ERROR! Cannot connect to the Server")
            exit()

        r1 = conn.getresponse()
        print(f"Response received!: {r1.status} {r1.reason}\n")

        response = json.loads(r1.read().decode("utf-8"))

        return response

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green', force_color=True)

        command = self.requestline.split(" ")[1].replace("/info", "").replace(".html", "")
        command2 = command.split("?")[0]

        ENDPOINT = "/info/species"
        s = ServerFormat(ENDPOINT)
        response_species = s.get_response()

        if command == "/" or command == "/index":
            contents = open("html/index.html", "r").read()
            content_type = 'text/html'


        elif command2 == "/listSpecies":
            length = len(response_species["species"])
            limit = command.split("=")[1].strip()
            if limit != "":
                try:
                    limit = int(limit)
                except ValueError:
                    limit = "error"

            list_species = []
            for i in range(0, length):
                list_species.append(response_species["species"][i]["display_name"])
            species = sorted(list_species)

            if limit != "" and limit != "error" and 0 <= limit <= length:
                species = species[:limit]
            elif limit == "error":
                species = "Unusual limit"
            else:
                species = "Limit out of range"

            contents = read_html_file("listSpecies.html").render(context={"todisplay": length, "todisplay2": limit, "todisplay3": species})
            content_type = 'text/html'


        elif command2 == "/Karyotype":
            common_name = command.split("=")[1].strip()
            common_name = common_name.replace("+", " ").strip().lower()

            species_list = []
            for e in response_species["species"]:
                species_list.append(e["display_name"].lower())
                if e["display_name"].strip().lower() == common_name:
                    species_name = e["name"]

                    ENDPOINT = "/info/assembly/" + species_name
                    s = ServerFormat(ENDPOINT)
                    response = s.get_response()

                    karyotype = response["karyotype"]

                    contents = read_html_file("Karyotype.html").render(context={"todisplay": karyotype})
                    content_type = 'text/html'

            existance = specie_exist(species_list, common_name)
            if existance != True:
                contents = open("html/error.html", "r").read()
                error_code = 200
                content_type = 'text/html'


        elif command2 == "/chromosomeLength":
            command = command.split("?")[1]
            specie = command.split("=")[1].split("&")[0].replace("+", " ").strip()
            chromosome = int(command.split("=")[2].strip())

            for e in response_species["species"]:
                if e["display_name"].strip().lower() == specie:
                    species_name = e["name"]

                    ENDPOINT = "/info/assembly/" + species_name
                    s = ServerFormat(ENDPOINT)
                    response = s.get_response()

                    length = response["top_level_region"][chromosome]["length"]

            contents = read_html_file("chromosomeLength.html").render(context={"todisplay": length})

            content_type = 'text/html'


        elif command2 == "/geneSeq":
            gene = command.split("=")[1]

            ENDPOINT = "/lookup/symbol/homo_sapiens/" + gene
            s = ServerFormat(ENDPOINT)
            response = s.get_response()

            id = response["id"]

            ENDPOINT = "/sequence/id/" + id
            s = ServerFormat(ENDPOINT)
            response = s.get_response()

            sequence = response["seq"]

            contents = read_html_file("geneSeq.html").render(context={"todisplay": sequence})

            content_type = 'text/html'


        elif command2 == "/geneInfo":
            gene = command.split("=")[1]

            ENDPOINT = "/lookup/symbol/homo_sapiens/" + gene
            s = ServerFormat(ENDPOINT)
            response = s.get_response()

            start = response["start"]
            end = response["end"]
            id = response["id"]
            print(response)

            ENDPOINT = "/sequence/id/" + id
            s = ServerFormat(ENDPOINT)
            response = s.get_response()

            sequence = response["seq"]
            length = len(sequence)

            contents = read_html_file("geneInfo.html").render(context={"start": start, "end": end, "length": length, "id": id, "chromosome_name": gene})
            content_type = 'text/html'


        elif command2 == "/geneCalc":
            gene = command.split("=")[1]
            ENDPOINT = "/lookup/symbol/homo_sapiens/" + gene
            s = ServerFormat(ENDPOINT)
            response = s.get_response()

            id = response["id"]

            ENDPOINT = "/sequence/id/" + id
            s = ServerFormat(ENDPOINT)
            response = s.get_response()

            sequence = response["seq"]
            length = len(sequence)

            s2 = Seq(sequence)
            bases_percent = s2.bases_percentage()[1]

            contents = read_html_file("geneCalc.html").render(context={"length": length, "A": bases_percent["A"], "C": bases_percent["C"], "G": bases_percent["G"], "T": bases_percent["T"]})
            content_type = 'text/html'


        else:
            contents = open("html/error.html", "r").read()
            content_type = 'text/html'

        self.send_response(404)

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