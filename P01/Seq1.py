class Seq:
    def __init__(self, seq=None):
        self.seq = seq

        if seq == None:
            print('NULL sequence created')
        else:
            check = self.check()
            if check == True:
                print('New sequence is created!')

            else:
                self.seq = 'ERROR'
                print('INVALID sequence!')

    def __str__(self):
        return self.seq

    def check(self):
        length = len(self.seq)
        count = 0
        for e in self.seq:
            if e in ['A', 'T', 'G', 'C']:
                count += 1
        if count == length:
            result = True
        else:
            result = False
        return result

    def seq_len(self):
        if self.seq == None or self.seq == 'ERROR':
            length = 0
        else:
            length = len(self.seq)
        return length

    def print_seqs(self):
        for i in range(0, len(self.seq)):
            print('Sequence', str(i) + ':', '(Length:', str(len(self.seq[i])) + ')', self.seq[i])

    def seq_count(self):
        length = self.seq_len()
        bases_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
        if length != 0:
            for e in self.seq:
                bases_dict[e] += 1
        return bases_dict

    def seq_reverse(self):
        if self.seq != None and self.seq != 'ERROR':
            reverse = self.seq[::-1]
        else:
            reverse = self.seq
        return reverse

    def seq_complement(self):
        if self.seq != None and self.seq != 'ERROR':
            complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
            complement_seq = ''
            for e in self.seq:
                complement_seq += complement_dict[e]
        else:
            complement_seq = self.seq
        complement_seq = complement_seq + "\n"
        return complement_seq

    def seq_read_fasta(self, filename):
        with open(filename, 'r') as f:
            seq = ''

            for line in f:
                for e in line:
                    seq += e

        index = seq.index('\n')
        seq = seq[index:]
        seq = seq.replace('\n', '')
        self.seq = seq
        return seq

    def frequent_base(self):
        count_dict = self.seq_count()
        values = count_dict.values()
        max_value = max(values)

        for e in count_dict:
            if count_dict[e] == max_value:
                result = e
        return result

    #def bases_percentage(self):
        #length = self.seq_len()
        #bases_dict = {"A": 0, "T": 0, "C": 0, "G": 0}
        #bases_percent = {"A": 0, "T": 0, "C": 0, "G": 0}

        #if length != 0:
            #for e in self.seq:
                #bases_dict[e] += 1
            #for e in bases_dict:
                #bases_percent[e] = str(round((bases_dict[e] / length * 100), 1)) + "%"

        #return bases_dict, bases_percent



    #def PING(self):
        #return print(f"{Color.GREEN} PING command! {Color.END}")

    #def GET(self, msg):
        #print(f"{Color.YELLOW} GET {Color.END}")
        #index = msg[4]
        #seq_l = ["ACCTCCTCAGCAA", "GGATCTCGATCA", "CCCTAGCCCAAA", "TCCCTTTCCTT"]
        #return seq_l[index]


# Códigos ANSI para cambiar el color del texto
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'





def generate_seqs(pattern, number):
    seq_list = []
    for i in range(0, number):
        if i == 0:
            seq_list.append(pattern)
        else:
            seq_list.append(pattern + seq_list[i - 1])
    return seq_list
