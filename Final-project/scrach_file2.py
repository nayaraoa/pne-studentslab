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

#with open('json/species_list.json', 'r') as f:
#    species_dict = json.load(f)


#print(species_dict["species"][0])

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

    def create_server_format(self):
        SERVER = "rest.ensembl.org"
        PARAMS ="?content-type=application/json"
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
            length = len(response_species["species"])
            limit = command.split("=")[1].strip()
            if limit != "":
                try:
                    limit = int(limit)
                except ValueError:
                    limit = "error"

            species = []
            if limit != "" and limit != "error" and 0 <= limit <= length:
                for i in range(0, limit):
                    species.append(response_species["species"][i]["display_name"])
            elif limit == "":
                for e in response_species["species"]:
                    species.append(e["display_name"])
            elif limit == "error":
                species = "Unusual limit"
            else:
                species = "Limit out of range"


            contents = read_html_file("listSpecies.html").render(context={"todisplay": length, "todisplay2": limit, "todisplay3": species})
            content_type = 'text/html'
            error_code = 200


        elif command2 == "/Karyotype":
            common_name = command.split("=")[1].strip()
            common_name = common_name.replace("+", " ").strip().lower()

            species_list = []
            for e in response_species["species"]:
                species_list.append(e["display_name"].lower())
                if e["display_name"].strip().lower() == common_name:
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

                    contents = read_html_file("Karyotype.html").render(context={"todisplay": karyotype})
                    error_code = 200
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

                    length = response["top_level_region"][chromosome]["length"]



            contents = read_html_file("chromosomeLength.html").render(context={"todisplay": length})


            content_type = 'text/html'
            error_code = 200


        elif command2 == "/geneSeq":
            gene = command.split("=")[1]

            ENDPOINT = "/lookup/symbol/homo_sapiens/" + gene
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

            id = response["id"]

            ENDPOINT = "/sequence/id/" + id
            URL = SERVER + ENDPOINT + PARAMS

            print()
            print(f"Server: {SERVER}")
            print(f"URL: {URL}")

            conn = http.client.HTTPConnection(SERVER)

            try:
                conn.request("GET", ENDPOINT + PARAMS)
            except ConnectionRefusedError:
                print("ERROR! Cannot connect to the Server")
                exit()

            r2 = conn.getresponse()

            print(f"Response received!: {r2.status} {r2.reason}\n")

            response = json.loads(r2.read().decode("utf-8"))
            sequence = response["seq"]

            contents = read_html_file("geneSeq.html").render(context={"todisplay": sequence})

            content_type = 'text/html'
            error_code = 200

        elif command2 == "/geneInfo":
            gene = command.split("=")[1]

            ENDPOINT = "/lookup/symbol/homo_sapiens/" + gene
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
            start = response["start"]
            end = response["end"]
            id = response["id"]
            chromosome_name = response["logic_name"]   #I don´t know if this one is supposed to be the name
            print(response)

            ENDPOINT = "/sequence/id/" + id
            URL = SERVER + ENDPOINT + PARAMS

            print()
            print(f"Server: {SERVER}")
            print(f"URL: {URL}")

            conn = http.client.HTTPConnection(SERVER)

            try:
                conn.request("GET", ENDPOINT + PARAMS)
            except ConnectionRefusedError:
                print("ERROR! Cannot connect to the Server")
                exit()

            r2 = conn.getresponse()

            print(f"Response received!: {r2.status} {r2.reason}\n")

            response = json.loads(r2.read().decode("utf-8"))
            sequence = response["seq"]
            length = len(sequence)

            contents = read_html_file("geneInfo.html").render(context={"start": start, "end": end,"length": length, "id": id, "chromosome_name": chromosome_name })

            content_type = 'text/html'
            error_code = 200


        elif command2 == "/geneCalc":
            gene = command.split("=")[1]
            ENDPOINT = "/lookup/symbol/homo_sapiens/" + gene
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
            id = response["id"]

            ENDPOINT = "/sequence/id/" + id
            URL = SERVER + ENDPOINT + PARAMS

            print()
            print(f"Server: {SERVER}")
            print(f"URL: {URL}")

            conn = http.client.HTTPConnection(SERVER)

            try:
                conn.request("GET", ENDPOINT + PARAMS)
            except ConnectionRefusedError:
                print("ERROR! Cannot connect to the Server")
                exit()

            r2 = conn.getresponse()

            print(f"Response received!: {r2.status} {r2.reason}\n")

            response = json.loads(r2.read().decode("utf-8"))
            sequence = response["seq"]
            length = len(sequence)


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