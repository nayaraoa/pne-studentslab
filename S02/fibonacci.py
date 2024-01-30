n = []
for i in range (0, 11):
    if n == [] or len(n) == 1:
        n.append(i)
    else:
        n.append(n[-1] + n[-2])

print(n)