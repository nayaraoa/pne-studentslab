import http.server
import socketserver
import termcolor
import jinja2 as j
from pathlib import Path
import json
from pprint import pprint
from Seq1 import Seq
from urllib.parse import parse_qs, urlparse

IP = "127.0.0.1"
PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

genes_dict = {"FRAT1": "ENSG00000165879",
              "ADA": "ENSG00000196839",
              "FXN": "ENSG00000165060",
              "RNU6_269P": "ENSG00000212379",
              "MIR633": "ENSG00000207552",
              "TTTY4C": "ENSG00000228296",
              "RBMY2YP": "ENSG00000227633",
              "FGFR3": "ENSG00000068078",
              "KDR": "ENSG00000128052",
              "ANK2": "ENSG00000145362"}

human_chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "X", "Y", "MT"]


def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents

def specie_exist(list_species, name_specie):
    if name_specie.capitalize() in list_species:
        return True

class ServerFormat():
    def __init__(self, ENDPOINT, ADD = None):
        self.ENDPOINT = ENDPOINT
        self.ADD = ADD

    def get_response(self):
        SERVER = "rest.ensembl.org"
        PARAMS = "?content-type=application/json"
        URL = SERVER + self.ENDPOINT + PARAMS

        print(f"Server: {SERVER}")
        print(f"URL: {URL}")

        conn = http.client.HTTPConnection(SERVER)
        try:
            if self.ADD == None:
                conn.request("GET", self.ENDPOINT + PARAMS)
            else:
                conn.request("GET", self.ENDPOINT + PARAMS + self.ADD)
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

        url_path = urlparse(self.path)
        parsed_path = url_path.path
        parsed_path = parsed_path.replace(".html", "").replace("/info", "")
        parameters = parse_qs(url_path.query)

        print(" path: ", end="")
        pprint(parsed_path)
        print(" parameters: ", end="")
        pprint(parameters)


        if "gene" in parsed_path and parsed_path != "/geneList":
            gene = parameters["gene"][0]
            id = genes_dict[gene]
            ENDPOINT = "/sequence/id/" + id
            s = ServerFormat(ENDPOINT)
            response = s.get_response()
            sequence = response["seq"]

        elif not "gene" in parsed_path:
            ENDPOINT = "/info/species"
            s = ServerFormat(ENDPOINT)
            response_species = s.get_response()
            list_species = []
            for i in range(0, len(response_species["species"])):
                list_species.append(response_species["species"][i]["display_name"])
            species = sorted(list_species)


        if parsed_path == "/" or parsed_path == "/index" or parsed_path == "/info/index":
            contents = open("html/index.html", "r").read()
            content_type = 'text/html'


        elif parsed_path == "/listSpecies":
            length = len(response_species["species"])
            limit = parameters["limit"][0]

            if limit != "":
                try:
                    limit = int(limit)
                except ValueError:
                    limit = "error"

            if limit != "" and limit != "error" and 0 <= limit <= length:
                species = species[:limit]
                ERROR = False
            elif limit == "error":
                ERROR = True
                error = "Unusual limit"
            else:
                ERROR = True
                error = "Limit out of range"

            if ERROR:
                contents = read_html_file("error.html").render(context={"error": error})
            else:
                contents = read_html_file("listSpecies.html").render(
                    context={"length": length, "limit": limit, "species": species})
            content_type = 'text/html'


        elif parsed_path == "/Karyotype":
            specie = parameters["species"][0]

            existance = specie_exist(species, specie)
            if existance != True:
                error = "Species not found."
                contents = read_html_file("error.html").render(context={"error": error})
            else:
                species_list = []
                for e in response_species["species"]:
                    species_list.append(e["display_name"].lower())
                    if e["display_name"].strip().lower() == specie:
                        species_name = e["name"]

                        ENDPOINT = "/info/assembly/" + species_name
                        s = ServerFormat(ENDPOINT)
                        response = s.get_response()
                        karyotype = response["karyotype"]
                contents = read_html_file("Karyotype.html").render(context={"karyotype": karyotype})
            content_type = 'text/html'


        elif parsed_path == "/chromosomeLength":
            specie = parameters["species"][0]
            chromosome = int(parameters["chromosome"][0])

            existance = specie_exist(species, specie)
            if existance != True:
                error = "Species not found."
                contents = read_html_file("error.html").render(context={"error": error})
            else:
                for e in response_species["species"]:
                    if e["display_name"].strip().lower() == specie:
                        species_name = e["name"]

                        ENDPOINT = "/info/assembly/" + species_name
                        s = ServerFormat(ENDPOINT)
                        response = s.get_response()
                        try:
                            length = response["top_level_region"][chromosome]["length"]
                            contents = read_html_file("chromosomeLength.html").render(context={"todisplay": length})
                        except IndexError:
                            error = f"The chromosome {chromosome} does not exist."
                            contents = read_html_file("error.html").render(context={"error": error})
            content_type = 'text/html'


        elif parsed_path == "/geneSeq":
            contents = read_html_file("geneSeq.html").render(context={"todisplay": sequence})
            content_type = 'text/html'


        elif parsed_path == "/geneInfo":
            ENDPOINT = "/lookup/symbol/homo_sapiens/" + gene
            s = ServerFormat(ENDPOINT)
            response = s.get_response()

            start = response["start"]
            end = response["end"]

            length = len(sequence)
            contents = read_html_file("geneInfo.html").render(
                context={"start": start, "end": end, "length": length, "id": id, "chromosome_name": gene})
            content_type = 'text/html'


        elif parsed_path == "/geneCalc":
            length = len(sequence)
            s2 = Seq(sequence)
            bases_percent = s2.bases_percentage()[1]

            contents = read_html_file("geneCalc.html").render(
                context={"length": length, "A": bases_percent["A"], "C": bases_percent["C"], "G": bases_percent["G"],
                         "T": bases_percent["T"]})
            content_type = 'text/html'


        elif parsed_path == "/geneList":
            chromosome = parameters["chromosome"][0]
            start = parameters["start"][0]
            end = parameters["end"][0]

            if chromosome not in human_chromosomes:
                error = "Chromosome not found."
                ERROR = True
            elif int(start) >= int(end) or int(start) <= 0:
                error = "Unvalid error and/or start"
                ERROR = True
            else:
                ERROR = False

            ENDPOINT = "/overlap/region/human/" + chromosome + ":" + start + "-" + end
            s = ServerFormat(ENDPOINT, ";feature=gene")
            response = s.get_response()

            pprint(response)

            gene_list = []
            for i in range(int(start), int(end)):
                gene_list.append(response[i]["external_name"])

            if ERROR:
                contents = read_html_file("error.html").render(context={"error": error})
            else:
                contents = read_html_file("geneList.html").render(context={"start": start, "end": end, "gene_list": gene_list})
            content_type = 'text/html'


        else:
            error = "Resource not found."
            contents = read_html_file("error.html").render(context={"error": error})
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

    # -- Main loop: Attend the client. Whenever there is a new client, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
