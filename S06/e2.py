class Seq:
    def __init__(self, seq): #self se pone siempre pero no es un nombre al que se le de un valor cuando nombramos la funcion, se le da el vlaaor directamente a seq_list en este caso
        self.seq = seq

    def len(self):
        return len(self.seq)


seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

print(f"Sequence 1: (Length: {seq_list[0].len()}) {seq_list[0].seq} ")
print(f"Sequence 2: (Length: {seq_list[1].len()}) {seq_list[1].seq}")
print(f"Sequence 5: (Length: {seq_list[2].len()}) {seq_list[2].seq}")


#the way is asked:
seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]
def print_seqs(seq_list):
    for i in range (0, len(seq_list)):
        print('Sequence', str(i) + ':', '(Length:', str(len(seq_list[i].seq)) + ')', seq_list[i].seq)

print_seqs(seq_list)



