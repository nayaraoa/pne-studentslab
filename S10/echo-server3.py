import socket
from pprint import pprint

PORT = 8082
IP = "212.128.255.80"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen()

print("The server is configured!")

connections = 0
clients_info = {}

while True:
    print("Waiting for clients ot connect.")


    try:
        (rs, address) = s.accept()
    except KeyboardInterrupt:
        print("Server stopped")
        print("The following clients have connected to the server:")
        for e in clients_info:
            print(e, clients_info[e])

        s.close()
        exit()

    else:
        connections += 1
        clients_info[f"Client {connections}"] = address
        print('A client has connected')
        print(f"CONNECTION {connections}. Client IP, PORT {address}")

        msg = rs.recv(2048).decode("utf-8")

        print(f"The client says {msg}")

        response = f"ECHO: {msg}"
        rs.send(response.encode())

        rs.close()

