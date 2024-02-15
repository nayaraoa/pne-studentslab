from Seq1 import Seq

s = Seq()
s = Seq(s.seq_read_fasta('U5.txt'))

print(f'Sequence 1: (Length: {s.seq_len()}) {s.seq}')
print('  Bases:', s.seq_count())
print('  Rev:', s.seq_reverse())
print('  Comp:', s.seq_complement())