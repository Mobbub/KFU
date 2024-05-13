def f(x):
    return x ** 2

def centr_prym(a, b, n):
    h = (b - a) / n
    integ = 0
    for i in range(n):
        xi = a +  i * h + h / 2
        integ += f(xi)
    integ *= h
    return integ
    
a = 0
b = 1
n = 7

print(centr_prym(a, b, n))