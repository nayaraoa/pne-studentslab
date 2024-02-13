
def print_seqs(seq_list):
    for seq in seq_list:
        length = len(seq)
    return length


class Seq:
    """A class for representing sequences"""
    def __init__(self, seq_list):
        for e in seq_list:
            self.seq_list = e
            print('New sequence is created!')




seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

print(f"Sequence 1: {s1.strbases} ")
print(f"Sequence 2: {s2}")
