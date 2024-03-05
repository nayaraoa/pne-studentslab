from Client0 import Client

PORT = 8082
IP = "212.128.255.80"

c = Client(IP, PORT)

for i in range(0, 5):
    print(c.talk(f"Message {i}"))