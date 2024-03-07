#francisco.romero@urjc.es

#client uses only one socket to connect to a server. In the case of the servers they need two sockets: one for listenning
# to connections, and another for transferring the data from/to the client

#When we already have one client connected and a second one connects, a new socket is created automatically.

#SETTING UP A SERVER
#  Step 1: Create the socket (method socket())
#  Step 2: Configure the socket: bind it to the IP and PORT (method bind()
#  Step 3: Configure the socket in listening mode (method listen())
#  Main loop:
#      Step 5: Wait for a client to connect (method accept()
#      Step 6: When a client connects, the socket library creates a new socket for communicating with the client
#      Step 7: Read the client's messages. What does the client want? (method recv())
#      Step 8: Process the request and send a response message (method send())


#hostname -1 para saber el public IP y el private IP

#how to write ourselfs: echo "Hi!" | nc IP PORT

hello = "HELLO"
print(hello[:2])