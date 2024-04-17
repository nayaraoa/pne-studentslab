from Seq1 import *
import http.client
import json
import termcolor

genes = {"FRAT1": "ENSG00000165879",
         "ADA": "ENSG00000196839",
         "FXN": "ENSG00000165060",
         "RNU6_269P": "ENSG00000212379",
         "MIR633": "ENSG00000207552",
         "TTTY4C": "ENSG00000228296",
         "RBMY2YP": "ENSG00000227633",
         "FGFR3": "ENSG00000068078",
         "KDR": "ENSG00000128052",
         "ANK2": "ENSG00000145362"}

gene_l = list(genes.keys())

for e in gene_l:
    id = genes[e]

    SERVER = "rest.ensembl.org"
    ENDPOINT = "/sequence/id/" + id
    PARAMS = "?content-type=application/json"
    URL = SERVER + ENDPOINT + PARAMS

    print()
    print(f"Server: {SERVER}")
    print(f"URL: {URL}")

    conn = http.client. HTTPConnection(SERVER)

    try:
        conn.request("GET", ENDPOINT + PARAMS)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    # -- Read the response message from the server
    r1 = conn.getresponse()

    # -- Print the status line
    print(f"Response received!: {r1.status} {r1.reason}\n")

    # -- Read the response's body
    response = json.loads(r1.read().decode("utf-8"))   #response= {'ping': 1}

    termcolor.cprint("Gene: ", 'green', end="", force_color=True)
    print(e)

    termcolor.cprint("Description: ", 'green', end="", force_color=True)
    print(response["desc"])

    s = Seq(response["seq"])

    termcolor.cprint("Total length: ", 'green', end="", force_color=True)
    print(s.seq_len())

    bases_dict, bases_percent = s.bases_percentage()
    for b in bases_dict:
        termcolor.cprint(f"{b}: ", 'blue', end="", force_color=True)
        print(bases_dict[b], f"({bases_percent[b]})")

    termcolor.cprint("Most frequent Base: ", 'green', end="", force_color=True)
    print(s.frequent_base())
