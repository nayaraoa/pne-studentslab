import socket

# Configure the Server's IP and PORT
PORT = 8081
IP = "212.128.255.80" # this IP address is local, so only requests from the same machine are possible

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening
ls.listen()

print("The server is configured!")

print("Waiting for clients ot connect.")
while True:
    (rs, address) = ls.accept() #to accept different clients into the server and returns a touple with the  and the IP
    print(f"Client {address}")

    msg = rs.recv(2048).decode("utf-8")

    print(f"The client says {msg}")

    response = "I'm a happy server"
    rs.send(response.encode())

    rs.close()

# -- Close the socket
ls.close()
