import numpy as np

def f(x):
    return x**2

def montecarlo(a, b, n):
    integ1 = 0
    for i in range(n):
        x = np.random.uniform(a, b)
        integ1 += f(x)
    integ = (b - a) / n * integ1
    return integ

a = 0
b = 1
n = 100

print(montecarlo(a, b, n))