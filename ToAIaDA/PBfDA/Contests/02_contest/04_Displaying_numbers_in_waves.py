def volna(n):
    num = 1
    for i in range(n):
        x = int(i**.5 + .5)
        k = x + 1 - abs(i - 1 - x ** 2)
        for j in range(k):
            if num <= n:
                print(num, end=' ')
            num += 1
        print()

n = int(input())
num = 1

if n == 1:
    print(1)
elif n == 2:
    print(1)
    print(2)
else:
    volna(n)