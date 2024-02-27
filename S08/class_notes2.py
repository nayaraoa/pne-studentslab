# ping (followed by the ip addres or the name of the url) to check the connectivity of a computer
# ifconfig to see our ip address (writen on the enp0s31f6 paragraph and after inet)
#DNS (domain name system) translates the URLs into IP (this way we dont need to learn the IP to search a web on internet, just the urls name)
# We use the port to identify a service (or app) and the IP to identify the machine
# 80port is reserved for web servers
# For communicating with a program that is running in another computer we use sockets.


import socket

# Configure the Server's IP and PORT
PORT = 8081
IP = "192.168.124.179" # it depends on the machine the server is running
MAX_OPEN_REQUESTS = 5

# Counting the number of connections
number_con = 0

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((IP, PORT))
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # accept connections from outside
        print("Waiting for connections at {}, {} ".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        # Another connection!e
        number_con += 1

        # Print the connection number
        print("CONNECTION: {}. From the IP: {}".format(number_con, address))

        # Read the message from the client, if any
        msg = clientsocket.recv(2048).decode("utf-8")
        print("Message from client: {}".format(msg))

        # Send the message
        message = "Hello from the teacher's server\n"
        send_bytes = str.encode(message)
        # We must write bytes, not a string
        clientsocket.send(send_bytes)
        clientsocket.close()

except socket.error:
    print("Problems using ip {} port {}. Is the IP correct? Do you have port permission?".format(IP, PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()

# printf '...' | nc IP PORT <-- esto lo escribimos en la terminal para mandar un mensaje al otro server



