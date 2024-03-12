from Client0 import Client

IP = "212.128.255.79"
PORT = 8080

c = Client(IP, PORT)

response = c.talk("32")
print(response)
