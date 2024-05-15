from server import ServerFormat
import json
from http import HTTPStatus
import requests

GENES = ["FRAT1", "RNU6_269P", "TP53", "BRCA1", "BRCA2", "EGFR", "ACTB", "GAPDH", "HBB", "CFTR", "INS", "TNF", "IL6", "VEGFA",
         "APOE", "MTOR", "ESR1", "CDKN1A", "FTO", "PTEN", "RB1", "KIT", "JAK2", "FOXP3", "MYC", "KRAS", "MAPK1",
         "SLC2A4", "ALB", "TTN", "COL1A1", "ELN", "RB1", "ACE", "MTHFR", "P53", "CCND1", "BCL2", "APC", "SERPINA1",
         "SOD1", "G6PD", "TGFBR2", "ATM", "PDGFRA", "CDH1", "GHR", "HLA-A", "SLC6A4", "NOS3", "DRD2", "PAX6"]

def server_request(server, url):
    import http.client

    error = False
    data = None
    try:
        connection = http.client.HTTPSConnection(server)
        connection.request("GET", url)
        response = connection.getresponse()
        if response.status == HTTPStatus.OK:
            json_str = response.read().decode()
            data = json.loads(json_str)
        else:
            error = True
    except Exception:  # Comment
        error = True
    return error, data

dict_genes_id = {}

for gene in GENES:
    PARAMS = "?content-type=application/json"
    ENDPOINT = "/homology/symbol/human/" + gene
    URL = "https://rest.ensembl.org" + ENDPOINT + PARAMS

    response = requests.get(URL)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # La solicitud fue exitosa
        data = response.json()# Convertir la respuesta JSON en un diccionario Python
        data = data["data"][0]

        # Verificar si hay datos en la respuesta
        if "id" in data:
            gene_id = data["id"]
            dict_genes_id[gene] = gene_id
        else:
            print("No se encontraron datos para el gen:", gene)
    else:
        # La solicitud falló
        print("Error al obtener datos para el gen:", gene, "Error:", response.status_code)

print(dict_genes_id)
