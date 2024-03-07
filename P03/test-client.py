import socket
from Client0 import Client

PRACTICE = 3
EXERCISE = 7

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

PORT = 8080
IP = "127.0.0.1"

c = Client(IP, PORT)

print("* Testing PING...")
response = c.talk('PING')
print(response)

print("* Testing GET...")
get_list = ["GET 0", "GET 1", "GET 2", "GET 3", "GET 4"]
for e in get_list:
    response = c.talk(e)
    print(f"{e}: {response}")


print("* Testing INFO...")
sequence =  "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"
print(f"Sequence: {sequence}")
print(f"Total length: {len(sequence)}")
response = c.talk("INFO ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA")
print(response)

print("* Testing COMP...")
print("COMP ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA")
response = c.talk("COMP ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA")
print(response)

print("* Testing REV...")
print("REV ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA")
response = c.talk("REV ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA")
print(response)

print("* Testing GENE...")
gene_list = ["GENE U5", "GENE ADA", "GENE FRAT1", "GENE FXN", "GENE RNU6_269P"]
for e in gene_list:
    response = c.talk(e)
    print(response)



