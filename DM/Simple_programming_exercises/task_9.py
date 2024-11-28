class Frac:
    def __init__(self, numerator, denominator):
        # Инициализация обыкновенной дроби с числителем и знаменателем
        self.numerator = numerator
        self.denominator = denominator
    
    @staticmethod
    def find_lcm(a, b):
        # Находит наименьшее общее кратное (НОК) двух чисел
        a, b = abs(a), abs(b)  # Берем абсолютные значения
        return (a * b) / Frac.find_gdc(a, b)  # НОК = (a * b) / НОД
    
    @staticmethod
    def find_gdc(a, b):
        # Находит наибольший общий делитель (НОД) двух чисел
        a, b = abs(a), abs(b)  # Берем абсолютные значения
        while b != 0:
            a, b = b, a % b  # Применяем алгоритм Евклида
        return a  # Возвращаем НОД
        
    def reverse(self):
        # Переворачивает дробь (меняет местами числитель и знаменатель)
        self.numerator, self.denominator = self.denominator, self.numerator
    
    def common_denominator(self, other):
        # Приводит дроби к общему знаменателю
        shared_denominator = Frac.find_lcm(self.denominator, other.denominator)  # Находим НОК знаменателей
        multiplier_a = shared_denominator / self.denominator  # Находим множитель для первой дроби
        multiplier_b = shared_denominator / other.denominator  # Находим множитель для второй дроби
        # Обновляем дроби с новым числителем и общим знаменателем
        self.__init__(self.numerator * multiplier_a, shared_denominator)
        other.__init__(other.numerator * multiplier_b, shared_denominator)

    def __add__(self, other):
        # Переопределяем оператор сложения дробей
        if self.denominator != other.denominator:  
            self.common_denominator(other)  # Приводим дроби к общему знаменателю, если они разные
        return Frac(self.numerator + other.numerator, self.denominator)  # Возвращаем новую дробь с суммой числителей
    
    def __mul__(self, other):
        # Переопределяем оператор умножения дробей
        return Frac(self.numerator * other.numerator, self.denominator * other.denominator)  # Умножаем числители и знаменатели
    
    def __invert__(self):
        # Переопределяем оператор обращения дроби
        return Frac(self.denominator, self.numerator)  # Возвращаем дробь с перевернутыми местами числителем и знаменателем
    
    def __str__(self):
        # Переопределяем строковое представление дроби
        return f"{self.numerator}/{self.denominator}"

# Пример использования класса Frac

# Создание обыкновенных дробей
frac1 = Frac(-1, 4)  # Первая дробь (-1/4)
frac2 = Frac(2, 3)   # Вторая дробь (2/3)

# Сложение дробей
result_add = frac1 + frac2  # Сложение двух дробей
print("Сумма дробей: ", result_add)  # Выводим результат сложения

# Умножение дробей
result_mul = frac1 * frac2  # Умножение двух дробей
print("Произведение дробей: ", result_mul)  # Выводим результат умножения

# Обращение дроби
result_invert = ~frac1  # Обращение первой дроби
result2_invert = ~frac2  # Обращение второй дроби
print("Обращение дробей: ", result_invert, " и ", result2_invert)  # Выводим результат обращения дробей