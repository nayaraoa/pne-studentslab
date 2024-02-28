from Seq1 import Seq
from Client0 import Client

PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "127.0.0.1" # your IP address
PORT = 8080
PORT2 = 8081

c = Client(IP, PORT)
c2 = Client(IP, PORT2)
print(c)
print(c2)


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
        elif len(sequences) == 10:
            correct = True
        else:
            sequences.append(sequence)
            sequence = ""

print("Gen FRAT1:", seq)
c.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases...")
c2.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases...")


def even(number):
    return int(number) % 2 == 0

for e in sequences:
    number = str(sequences.index(e) + 1)
    print("Fragment", number, ":", e)
    if not even(number):
        c.talk("Fragment " + number + " : " + e)
    else:
        c2.talk("Fragment " + number + " : " + e)
