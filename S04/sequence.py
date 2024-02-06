from pathlib import Path

filename = 'sequences/ADA.txt'
file_contents = Path(filename).read_text()

list_contents = file_contents.split('\n')

body_seq = ''

for i in range (1, len(list_contents)):
    body_seq += list_contents[i]

print(len(body_seq))