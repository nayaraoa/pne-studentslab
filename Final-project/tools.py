import json
import http.client
import jinja2 as j
from pathlib import Path
import http.server
from http import HTTPStatus

GENES = ["FRAT1", "RNU6_269P", "TP53", "BRCA1", "BRCA2", "EGFR", "ACTB", "GAPDH", "HBB", "CFTR", "INS", "TNF", "IL6", "VEGFA",
         "APOE", "MTOR", "ESR1", "CDKN1A", "FTO", "PTEN", "RB1", "KIT", "JAK2", "FOXP3", "MYC", "KRAS", "MAPK1",
         "SLC2A4", "ALB", "TTN", "COL1A1", "ELN", "RB1", "ACE", "MTHFR", "P53", "CCND1", "BCL2", "APC", "SERPINA1",
         "SOD1", "G6PD", "TGFBR2", "ATM", "PDGFRA", "CDH1", "GHR", "HLA-A", "SLC6A4", "NOS3", "DRD2", "PAX6"]

def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents


def specie_exist(list_species, name_specie):
    if name_specie.capitalize() in list_species:
        return True


def get_response(ENDPOINT, PARAMS_given=None):
    SERVER = "rest.ensembl.org"
    PARAMS = "?content-type=application/json"

    if PARAMS_given != None:
        URL = SERVER + ENDPOINT + PARAMS_given
    else:
        URL = SERVER + ENDPOINT + PARAMS

    print(f"Server: {SERVER}")
    print(f"URL: {URL}")

    conn = http.client.HTTPConnection(SERVER)
    try:
        if PARAMS_given != None:
            conn.request("GET", ENDPOINT + PARAMS_given)
        else:
            conn.request("GET", ENDPOINT + PARAMS)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    r1 = conn.getresponse()
    print(f"Response received!: {r1.status} {r1.reason}\n")
    response = json.loads(r1.read().decode("utf-8"))

    return response


def get_id(gene):
    SERVER = "rest.ensembl.org"
    PARAMS = "?content-type=application/json"
    ENDPOINT = "/homology/symbol/human/" + gene
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

    if r1.status == HTTPStatus.OK:
        id = response["data"][0]["id"]
        error = None
    else:
        id = None
        error = "Gene not found."

    return id, error


class Check_Parameter_Error():
    def Karyotype_error(self, parameters):
        if not "species" in parameters:
            ERROR = True
            error = "The species must be indicated."
        else:
            ERROR = False
            error = None
        return ERROR, error

    def chromosomeLenght_error(self, parameters):
        if not "species" in parameters:
            ERROR = True
            error = "The species must be indicated."
        elif not "chromosome" in parameters:
            ERROR = True
            error = "The chromosome must be indicated."
        else:
            ERROR = False
            error = None
        return ERROR, error

    def geneList_error(self, parameters):
        if not "start" in parameters:
            ERROR = True
            error = "The start must be indicated."
        elif not "chromosome" in parameters:
            ERROR = True
            error = "The chromosome must be indicated."
        elif not "end" in parameters:
            ERROR = True
            error = "The end must be indicated."
        else:
            ERROR = False
            error = None
        return ERROR, error

    def gene_seq_error(self, parameters):
        if not "gene" in parameters:
            ERROR = True
            error = "The gene must be indicated."
        else:
            ERROR = False
            error = None
        return ERROR, error