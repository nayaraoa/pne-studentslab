
class Seq:
    def __init__(self, seq):
        self.seq = seq
        print('New sequence created!')

    def print_seqs(self, color_code):
        for i in range(0, len(self.seq)):
            print('\033[' + color_code + 'm' + 'Sequence', str(i) + ':', '(Length:', str(len(self.seq[i])) + ')', self.seq[i], '\033[0m')

def generate_seqs(pattern, number):
    seq_list = []
    for i in range(0, number):
        if i == 0:
            seq_list.append(pattern)
        else:
            seq_list.append(pattern + seq_list[i-1])
    return seq_list

seq_list1 = Seq(generate_seqs("A", 3)).seq
seq_list2 = Seq(generate_seqs("AC", 5)).seq



print("\033[94mList 1:\033[0m")
Seq(seq_list1).print_seqs('94')

print("\033[92mList 2:\033[0m")
Seq(seq_list2).print_seqs('92')
