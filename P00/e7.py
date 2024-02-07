from Seq0 import *

fragment = seq_read_fasta('U5(2).txt')[:20]
print('Gene U5', '\n' + 'Frag:', fragment , '\n' + 'Comp:', seq_complement(fragment))
