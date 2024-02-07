from Seq0 import *

U5 = seq_read_fasta('U5(2).txt')
ADA = seq_read_fasta('ADA(2).txt')
FRAT1 = seq_read_fasta('FRAT1(2).txt')
FXN = seq_read_fasta('FXN(2).txt')

print('Gene U5:', seq_count(U5))
print('Gene ADA:', seq_count(ADA))
print('Gene FRAT1:', seq_count(FRAT1))
print('Gene FXN:', seq_count(FXN))