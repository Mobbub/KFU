import math
from math import *

def f(x):
    return sin(x)

def simp(a, b, n):
    h = (b - a) / n
    integ = f(a) + f(b)
    for i in range(1, n):
        integ += f(a + i * h) * (2 if i % 2 == 0 else 4)
    return integ * h / 3
    
a = 0
b = 1
n = 6

print(simp(a, b, n))