def seq_ping():
    print('OK')


def seq_read_fasta(filename):
    with open(filename, 'r') as f:
        seq = ''

        for line in f:
            for e in line:
                seq += e

    index = seq.index('\n')
    seq = seq[index:]
    seq = seq.replace('\n', '')
    return seq

def seq_len(seq):
    length = len(seq)
    return length


def seq_count_base(seq, base):
    count = 0
    for e in seq:
        if e == base:
            count += 1
    return count


def seq_count(seq):
    bases_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
    for e in seq:
        bases_dict[e] += 1
    return bases_dict


def seq_reverse(seq, n):
    fragment = seq[0:n]
    reverse = fragment[::-1]
    return reverse


def seq_complement(seq):
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    complement_seq = ''
    for e in seq:
        complement_seq += complement_dict[e]
    return complement_seq


def frequent_base(seq):
     count_dict = seq_count(seq)
     values = count_dict.values()
     max_value = max(values)

     for e in count_dict:
         if count_dict[e] == max_value:
             result = e
     return result
