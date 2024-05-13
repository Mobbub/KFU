def f(x):
    return x*2

def trap(a, b, n):
    h = (b - a) / n
    integ = 0
    for i in range(n):
        integ += h * (f(a) + f(a + h)) / 2
        a += h
    return integ

a = 0
b = 1
n = 10

print(trap(a, b, n))
