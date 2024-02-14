class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases):
        self.strbases = strbases
        check = self.check()
        if check == True:
            print('New sequence is created!')
        else:
            self.strbases = 'ERROR'
            print('ERROR!!')

    def check(self):
        length = len(self.strbases)
        count = 0
        for e in self.strbases:
            if e in ['A', 'T', 'G', 'C']:
                count += 1
        if count == length:
            result = True
        else:
            result = False
        return result

    def len(self):
        return len(self.seq)

    def print_seqs(self):
        for i in range(0, len(self.seq)):
            print('Sequence', str(i) + ':', '(Length:', str(len(self.seq[i])) + ')', self.seq[i])

def generate_seqs(pattern, number):
    seq_list = []
    for i in range(0, number):
        if i == 0:
            seq_list.append(pattern)
        else:
            seq_list.append(pattern + seq_list[i-1])
    return seq_list
