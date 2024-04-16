import http.client
import json
import termcolor

PORT = 8080
SERVER = 'localhost'

print(f"\nConnecting to server: {SERVER}:{PORT}\n")

# Connect with the server
conn = http.client.HTTPConnection(SERVER, PORT)

# -- Send the request message, using the GET method. We are
# -- requesting the page with the list of the users (/listusers)
try:
    conn.request("GET", "/listusers")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

# -- Read the response message from the server
r1 = conn.getresponse()

# -- Print the status line
print(f"Response received!: {r1.status} {r1.reason}\n")

# -- Read the response's body
data1 = r1.read().decode("utf-8")

# -- Create a variable with the data,
# -- form the JSON received. Creo que se crea un diccionario
people = json.loads(data1)

print("CONTENT: ")

for e in people["people"]:
    # Print the information in the object
    print()
    termcolor.cprint("Name: ", 'green', end="", force_color=True)
    print(e['Firstname'], e['Lastname'])

    termcolor.cprint("Age: ", 'green', end="", force_color=True)
    print(e['age'])

    # Get the phoneNumber list
    phoneNumbers = e['phoneNumber']

    # Print the number of elements int the list
    termcolor.cprint("Phone numbers: ", 'green', end='', force_color=True)
    print(len(phoneNumbers))

    # Print all the numbers
    for i, num in enumerate(phoneNumbers):
        termcolor.cprint("  Phone {}:".format(i), 'blue', force_color=True)

        # The element num contains 2 fields: number and type
        termcolor.cprint("    Type: ", 'red', end='', force_color=True)
        print(num['type'])
        termcolor.cprint("    Number: ", 'red', end='', force_color=True)
        print(num['number'])