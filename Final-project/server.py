import socketserver
import termcolor
from pprint import pprint
from Seq1 import Seq
from urllib.parse import parse_qs, urlparse
from tools import *
#I started to organize the advance level but i didn´t had time to finish it.

IP = "127.0.0.1"
PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

genes_dict = {"FRAT1": "ENSG00000165879", "ADA": "ENSG00000196839",
              "FXN": "ENSG00000165060", "RNU6_269P": "ENSG00000212379",
              "MIR633": "ENSG00000207552", "TTTY4C": "ENSG00000228296",
              "RBMY2YP": "ENSG00000227633", "FGFR3": "ENSG00000068078",
              "KDR": "ENSG00000128052", "ANK2": "ENSG00000145362",
              "TP53": "ENSG00000141510", "BRCA1": "ENSG00000012048",
              "BRCA2": "ENSG00000139618", "EGFR": "ENSG00000146648",
              "ACTB": "ENSG00000075624", "GAPDH": "ENSG00000111640",
              "HBB": "ENSG00000244734"
              }
human_chromosomes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "X", "Y", "MT"]

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green', force_color=True)

        url_path = urlparse(self.path)
        parsed_path = url_path.path
        parsed_path = parsed_path.replace(".html", "").replace("/info", "")
        parameters = parse_qs(url_path.query)

        json_parameter = parameters.get("json", [0])

        print(" path: ", end="")
        pprint(parsed_path)
        print(" parameters: ", end="")
        pprint(parameters)

        content_type = 'text/html'
        if json_parameter[0] == "1":
            JSON = True
            content_type = "application/json"

        if "gene" in parsed_path and parsed_path != "/geneList":
            s = Check_Parameter_Error()
            ERROR, error = s.gene_seq_error(parameters)

            if ERROR:
                contents = read_html_file("error.html").render(context={"error": error})
            else:
                gene = parameters["gene"][0]
                id, error = get_id(gene)

                if id != None:
                    ENDPOINT = "/sequence/id/" + id
                    response = get_response(ENDPOINT)
                    sequence = response["seq"]
                else:
                    ERROR = True
                    contents = read_html_file("error.html").render(context={"error": error})

        elif not "gene" in parsed_path:
            ENDPOINT = "/info/species"
            response_species = get_response(ENDPOINT)
            list_species = []
            for i in range(0, len(response_species["species"])):
                list_species.append(response_species["species"][i]["display_name"])
            species = sorted(list_species)


        if parsed_path == "/" or parsed_path == "/index" or parsed_path == "/info/index":
            contents = open("html/index.html", "r").read()


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


        elif parsed_path == "/Karyotype":
            s = Check_Parameter_Error()
            ERROR, error = s.Karyotype_error(parameters)

            if not ERROR:
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
                            response = get_response(ENDPOINT)
                            karyotype = response["karyotype"]
                    contents = read_html_file("Karyotype.html").render(context={"karyotype": karyotype})
            else:
                contents = read_html_file("error.html").render(context={"error": error})


        elif parsed_path == "/chromosomeLength":
            s = Check_Parameter_Error()
            ERROR, error = s.chromosomeLenght_error(parameters)

            if not ERROR:
                specie = parameters["species"][0]
                chromosome = parameters["chromosome"][0]

                existance = specie_exist(species, specie)
                if existance != True:
                    error = "Species not found."
                    contents = read_html_file("error.html").render(context={"error": error})
                else:
                    for e in response_species["species"]:
                        if e["display_name"].strip().lower() == specie:
                            species_name = e["name"]

                            ENDPOINT = "/info/assembly/" + species_name
                            response = get_response(ENDPOINT)
                            try:
                                length = response["top_level_region"][int(chromosome)]["length"]
                                contents = read_html_file("chromosomeLength.html").render(context={"todisplay": length})
                            except ValueError:
                                error = f"The chromosome '{chromosome}' does not exist."
                                contents = read_html_file("error.html").render(context={"error": error})
                            except IndexError:
                                error = f"The chromosome '{chromosome}' does not exist."
                                contents = read_html_file("error.html").render(context={"error": error})
            else:
                contents = read_html_file("error.html").render(context={"error": error})


        elif parsed_path == "/geneSeq":
            if not ERROR:
                contents = read_html_file("geneSeq.html").render(context={"todisplay": sequence})


        elif parsed_path == "/geneInfo":
            if not ERROR:
                ENDPOINT = "/lookup/symbol/homo_sapiens/" + gene
                response = get_response(ENDPOINT)
                ERROR2 = False

                try:
                    start = response["start"]
                    end = response["end"]
                except KeyError:
                    ERROR2 = True
                    error = "Gene not found."

                if not ERROR2:
                    length = len(sequence)
                    contents = read_html_file("geneInfo.html").render(
                        context={"start": start, "end": end, "length": length, "id": id, "chromosome_name": gene})
                else:
                    contents = read_html_file("error.html").render(context={"error": error})

        elif parsed_path == "/geneCalc":
            if not ERROR:
                length = len(sequence)
                s2 = Seq(sequence)
                bases_percent = s2.bases_percentage()[1]

                contents = read_html_file("geneCalc.html").render(
                    context={"length": length, "A": bases_percent["A"], "C": bases_percent["C"], "G": bases_percent["G"],
                             "T": bases_percent["T"]})


        elif parsed_path == "/geneList":
            s = Check_Parameter_Error()
            ERROR, error = s.geneList_error(parameters)

            if not ERROR:
                chromosome = parameters["chromosome"][0]
                start = parameters["start"][0]
                end = parameters["end"][0]

                if chromosome not in human_chromosomes:
                    error = f"Chromosome '{chromosome}' not found."
                    ERROR2 = True
                elif int(start) >= int(end) or int(start) <= 0:
                    error = "Unvalid end and/or start"
                    ERROR2 = True
                else:
                    ERROR2 = False

                if ERROR2:
                    contents = read_html_file("error.html").render(context={"error": error})
                else:
                    ENDPOINT = f"/overlap/region/human/{chromosome}:{start}-{end}"
                    PARAMS = "?feature=gene;feature=transcript;feature=cds;feature=exon;content-type=application/json"
                    response = get_response(ENDPOINT, PARAMS)

                    gene_list = []
                    for e in response:
                        if e["feature_type"] == "gene":
                            try:
                                gene_list.append(e["external_name"])
                            except KeyError:
                                pass
                    contents = read_html_file("geneList.html").render(context={"chromosome": chromosome, "start": start, "end": end, "gene_list": gene_list})
            else:
                contents = read_html_file("error.html").render(context={"error": error})


        else:
            error = "Resource not found."
            contents = read_html_file("error.html").render(context={"error": error})

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