import numpy as np

def f(x):
    return x ** 2

def gauss(a, b, n):
    t, a1 = np.polynomial.legendre.leggauss(n)
    integ = (b - a) / 2
    for i in range(n):
        integ += a1[i] * f((b - a) / 2 * t[i] + (a + b) / 2)
    return integ

a = 0
b = 1
n = 100

print(gauss(a, b, n))