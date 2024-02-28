from Seq1 import Seq

s1 = Seq()
s1 = Seq(s1.seq_read_fasta('U5.txt'))
print('Gene U5: Most frequent Base:', s1.frequent_base())

s2 = Seq()
s2 = Seq(s2.seq_read_fasta('ADA.txt'))
print('Gene ADA: Most frequent Base:', s2.frequent_base())

s3 = Seq()
s3 = Seq(s3.seq_read_fasta('FRAT1.txt.txt'))
print('Gene FRAT1.txt: Most frequent Base:', s3.frequent_base())

s4 = Seq()
s4 = Seq(s4.seq_read_fasta('RNU6_269P'))
print('Gene RNU6_269P: Most frequent Base:', s2.frequent_base())