
def fibo(n):
    l = []
    for i in range(0, n):
        if l == [] or len(l) == 1:
            l.append(i)
        else:
            l.append(l[-1] + l[-2])
    return l

print('5th fibonacci term:', fibo(6)[-1])
print('10th fibonacci term:', fibo(11)[-1])
print('15th fibonacci term:', fibo(16)[-1])