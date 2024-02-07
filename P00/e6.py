from Seq0 import *

fragment = seq_read_fasta('U5(2).txt')[:20]
print('Gene U5', '\n' + 'Fragment:', fragment, '\n' + 'Reverse:', seq_reverse(seq_read_fasta('U5(2).txt'), 20))