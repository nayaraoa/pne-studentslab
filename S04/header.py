from pathlib import Path

filename = '../sequences/RNU6_269P.txt'
file_contents = Path(filename).read_text()

list_contents = file_contents.split('\n')

print(list_contents[0])

