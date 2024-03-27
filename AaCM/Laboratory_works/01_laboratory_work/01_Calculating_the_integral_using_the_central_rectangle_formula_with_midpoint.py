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

# def trap(a, b, n):
#     h = (b - a) / n
#     integ = 0
#     for i in range(n):
#         integ += h * (f(a) + f(a + h)) / 2
#         a += h
#     return integ

# def simp(a, b, n):
#     h = (b - a) / n
#     integ = f(a) + f(b)
#     for i in range(1, n, 2):
#         integ += 4 * f(a + i * h)
#     for j in range(1, n - 1, 2):
#         integ += 2 * f(a + j * h)
#     integ *= h / 3
#     return integ

a = 0
b = 1
n = 1000

print(centr_prym(a, b, n))

# while True:
#     sposob = input('''Каким способом будем делать? (выбери цифру)
# 1. Через формулу центральных прямоугольников (со средней точкой).
# 2. Через формулу трапеций.
# 3. Через формулу Симпсона.
# ''')

#     if sposob == '1':
#         a = int(input('Введите начальное значение отрезка: '))
#         b = int(input('Введите конечное значение отрезка: '))
#         n = int(input('Введите количество разбиений данного отрезка: '))
#         print('Интеграл равен = ', centr_prym(a, b, n), '\n')
#     elif sposob == '2':
#         a = int(input('Введите начальное значение отрезка: '))
#         b = int(input('Введите конечное значение отрезка: '))
#         n = int(input('Введите количество разбиений данного отрезка: '))
#         print('Интеграл равен = ', trap(a, b, n), '\n')
#     elif sposob == '3':
#         a = int(input('Введите начальное значение отрезка: '))
#         b = int(input('Введите конечное значение отрезка: '))
#         n = int(input('Введите количество разбиений данного отрезка: '))
#         print('Интеграл равен = ', simp(a, b, n), '\n')
#     else:
#         print('Нет такого варианта ответа(')