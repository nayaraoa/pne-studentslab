from Seq0 import *

U5 = seq_read_fasta('U5(2).txt')
ADA = seq_read_fasta('ADA(2).txt')
FRAT1 = seq_read_fasta('FRAT1(2).txt')
FXN = seq_read_fasta('FXN(2).txt')

print('Gene U5: Most frequent Base:', frequent_base(U5), '\n' + 'Gene ADA: Most frequent Base:', frequent_base(ADA), '\n' + 'Gene FRAT1.txt: Most frequent Base:', frequent_base(FRAT1), '\n' + 'Gene FXN: Most frequent Base:', frequent_base(FXN))
