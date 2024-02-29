import socket

# SERVER IP, PORT
PORT = 8081
IP = "212.128.255.12"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

msg = input('Enter the message you want to send:')

s.send(str.encode(msg))

s.close()