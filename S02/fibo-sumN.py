def fibosum(n):
    l = []
    for i in range(0, n):
        if l == [] or len(l) == 1:
            l.append(i)
        else:
            l.append(l[-1] + l[-2])

    sum = 0
    for e in l:
        sum += e

    return sum

print('Sum of the first 5 terms of the Fibonacci series:', fibosum(6))
print('Sum of the first 5 terms of the Fibonacci series:', fibosum(11))
