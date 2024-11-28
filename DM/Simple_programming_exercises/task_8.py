def fibonacci_sequence(n):
    # Функция для вычисления n-го числа Фибоначчи
    if n <= 1:
        return n  # Базовые случаи: fib(0) = 0 и fib(1) = 1
    else:
        # Рекурсивный вызов для вычисления n-го числа как суммы двух предыдущих
        return (fibonacci_sequence(n-1) + fibonacci_sequence(n-2))

def fibonacci_partial_sums(n):
    # Функция для вычисления суммы первых n чисел Фибоначчи
    total = 0  # Инициализация переменной для суммы
    for i in range(n + 1):
        total += fibonacci_sequence(i)  # Суммируем числа Фибоначчи от 0 до n
    return total  # Возвращаем итоговую сумму

def find_index_by_digit_count(M, max_iterations=1000):
    # Функция для нахождения индекса первого числа Фибоначчи,
    # число цифр в котором превышает M
    index = 0  # Начальный индекс
    iterations = 0  # Счетчик итераций

    while iterations < max_iterations:
        partial_sum = fibonacci_partial_sums(index)  # Вычисляем частичную сумму
        num_digits = len(str(partial_sum))  # Находим количество цифр в этой сумме

        if num_digits > M:
            return index  # Возвращаем индекс, если количество цифр больше M

        index += 1  # Увеличиваем индекс для следующей итерации
        iterations += 1  # Увеличиваем счетчик итераций

    return -1  # Возвращаем -1, если решение не найдено за max_iterations

# Задаем значение M, количество цифр
M = 4
max_iterations = 1000  # Максимальное количество итераций для поиска
index = find_index_by_digit_count(M, max_iterations)  # Ищем индекс
if index == -1:
    print(f"Решение не найдено за {max_iterations} итераций.")  # Если решение не найдено
else:
    print(f"Индекс первого числа, количество цифр в котором больше {M}: {index}")  # Выводим найденный индекс
