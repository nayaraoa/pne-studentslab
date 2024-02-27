import socket

# SERVER IP, PORT
PORT = 8081
IP = "212.128.255.64" # depends on the computer the server is running
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serversocket.bind((IP, PORT))
    serversocket.listen()
    while True:
        msg = input('Enter the message you want to send:')

      # -- Establish the connection to the Server
        print("Waiting for connections at {}, {} ".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

      # -- Send the user message
        send_bytes = str.encode(msg)

      # -- Close the socket
        clientsocket.send(send_bytes)
        clientsocket.close()

except socket.error:
    print("Problems using ip {} port {}. Is the IP correct? Do you have port permission?".format(IP, PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()