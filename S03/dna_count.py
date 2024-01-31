
def count_dna_bases():
    seq = input('Please enter a DNA sequence:').strip()
    seq_dict = {'Total length': 0, 'A':0, 'C':0, 'T':0, 'G':0}
    for e in seq:
        seq_dict['Total length'] += 1
        seq_dict[e] += 1
    return seq_dict

seq_dict = count_dna_bases()
print('Total length:', seq_dict['Total length'])
print('A:', seq_dict['A'])
print('C:', seq_dict['C'])
print('T:', seq_dict['T'])
print('G:', seq_dict['G'])