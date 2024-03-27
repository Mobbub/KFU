def f(x):
    return x ** 2

def simp(a, b, n):
    h = (b - a) / n
    integ = f(a) + f(b)
    for i in range(1, n, 2):
        integ += 4 * f(a + i * h)
    for j in range(1, n - 1, 2):
        integ += 2 * f(a + j * h)
    integ *= h / 3
    return integ

a = 0
b = 1
n = 100

print(simp(a, b, n))
