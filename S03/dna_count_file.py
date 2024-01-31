def count_dna_bases(seq):
    seq_dict = {'Total length': 0, 'A':0, 'C':0, 'T':0, 'G':0}
    for e in seq:
        seq_dict['Total length'] += 1
        seq_dict[e] += 1
    return seq_dict

with open('dna.txt', 'r') as f:
    sequence = ''
    for e in f:
        for c in e:
            if c != '\n':
                sequence += (c)


seq_dict = count_dna_bases(sequence)
print(seq_dict)