from Seq1 import Seq
from Client0 import Client

PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "212.128.255.79" # your IP address
PORT = 8080

c = Client(IP, PORT)
print(c)


seq = Seq()
seq.seq_read_fasta("../sequences/FRAT1.txt")
seq = str(seq)

sequences = []
sequence = ""

correct = False
while not correct:
    for e in seq:
        if len(sequence) < 10:
            sequence += e
        elif len(sequences) == 5:
            correct = True
        else:
            sequences.append(sequence)
            sequence = ""

print("Gen FRAT1:", seq)
c.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases...")

for e in sequences:
    print("Fragment" + str(sequences.index(e) + 1) + ":", e)
    c.talk(e)














