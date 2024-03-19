from Client0 import Client

IP = "127.0.0.1"
PORT = 8081

c = Client(IP, PORT)

response = c.talk("5")
print(response)
