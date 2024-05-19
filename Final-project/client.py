import http.client
import json
from tools import *

#(It is not finished)

SERVER = "rest.ensembl.org"

ENDPOINT_dict = {}

class client:
    def __init__ (self):
        print()
        print(f"Server: {SERVER}")

    def send_request(self, PARAMS_geneList = None):
        if PARAMS_geneList == None:
            PARAMS = "?content-type=application/json"
        else:
            PARAMS = "?feature=gene;feature=transcript;feature=cds;feature=exon;content-type=application/json"

        conn = http.client. HTTPConnection(SERVER)

        try:
            conn.request("GET", ENDPOINT + PARAMS)
        except ConnectionRefusedError:
            print("ERROR! Cannot connect to the Server")
            exit()

        r1 = conn.getresponse()
        print(f"Response received!: {r1.status} {r1.reason}\n")
        response = json.loads(r1.read().decode("utf-8"))
