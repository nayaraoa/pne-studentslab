from Seq1 import Seq
from Client0 import Client

genes = ["U5", "FRAT1", "ADA"]

PRACTICE = 2
EXERCISE = 4

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "212.128.255.79" # your IP address
PORT = 8080

c = Client(IP, PORT)
print(c)


for g in genes:
    filename = "../sequences/" + g + ".txt"
    seq = Seq()
    seq.seq_read_fasta(filename)

    msg = "Sending " + g + " Gene to the server..."

    print('To Server:' + msg)
    print('Response:' + c.talk(msg))

    print('To Server:' + str(seq))
    print('Response:' + c.talk(str(seq)))

