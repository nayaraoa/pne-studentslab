from Seq1 import Seq

s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")

print(f'Sequence 1: (Length: {s1.seq_len()}) {s1.seq}')
print('  Bases:', s1.seq_count())
print(f'Sequence 2: (Length: {s2.seq_len()}) {s2.seq}')
print('  Bases:', s2.seq_count())
print(f'Sequence 3: (Length: {s3.seq_len()}) {s3.seq}')
print('  Bases:', s3.seq_count())
