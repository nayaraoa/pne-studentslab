from Client0 import Client
PRACTICE = 2
EXERCISE = 1

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "212.128.255.80" # your IP address
PORT = 8081

c = Client(IP, PORT)

c.ping()
