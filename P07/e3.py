import http.client
import json
import termcolor

SERVER = "rest.ensembl.org"
ENDPOINT = "/sequence/id/ENSG00000207552"
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

termcolor.cprint("Gene:", 'green', end="", force_color=True)
print("MIR633")

termcolor.cprint("Description:", 'green', end="", force_color=True)
print(response["desc"])

termcolor.cprint("Gene:", 'green', end="", force_color=True)
print(response["seq"])