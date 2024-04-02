def f(x):
    return x ** 2

def simp(a, b, n):
    h = float(b - a) / n
    integ = func(a) + func(b)
    for i in range(1, n):
        integ += func(a + i * h) * (2 if i % 2 == 0 else 4)
    return integ * h / 3
    
a = 0
b = 1
n = 100

print(simp(a, b, n))
