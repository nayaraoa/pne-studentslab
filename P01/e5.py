from Seq1 import Seq

s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")

print(f'Sequence 1: (Length: {s1.seq_len()}) {s1.seq}')
print('  A:', (s1.seq_count())['A'], '  T:', (s1.seq_count())['T'], '  C:', (s1.seq_count())['C'], '  G:', (s1.seq_count())['G'])

print(f'Sequence 2: (Length: {s2.seq_len()}) {s2.seq}')
print('  A:', (s2.seq_count())['A'], '  T:', (s2.seq_count())['T'], '  C:', (s2.seq_count())['C'], '  G:', (s2.seq_count())['G'])

print(f'Sequence 1: (Length: {s3.seq_len()}) {s3.seq}')
print('  A:', (s3.seq_count())['A'], '  T:', (s3.seq_count())['T'], '  C:', (s3.seq_count())['C'], '  G:', (s3.seq_count())['G'])