from math import sqrt, acos, pi

class Descr:
    def __init__(self):
        # Инициализация объекта Descr, сохранение вершин четырехугольника
        self.vertices = self.get_vertices()

    def __str__(self):
        # Возвращает строковое представление вершин четырехугольника
        return str(self.vertices)

    def __eq__(self, other):
        # Переопределение оператора == для сравнения двух четырехугольников
        if not isinstance(other, Descr):
            return False  # Проверка на то, что другой объект также является Descr

        # Получение длин сторон текущего четырехугольника
        a1, b1, c1, d1 = self.get_side_lengths()
        # Получение длин сторон другого четырехугольника
        a2, b2, c2, d2 = other.get_side_lengths()
        # Получение углов текущего четырехугольника
        angle1, angle2, angle3, angle4 = self.get_angles()
        # Получение углов другого четырехугольника
        angle1_other, angle2_other, angle3_other, angle4_other = other.get_angles()

        # Проверяем равенство длин сторон и величин углов
        return (a1 == a2 and b1 == b2 and c1 == c2 and d1 == d2) and (angle1 == angle1_other and angle2 == angle2_other and angle3 == angle3_other and angle4 == angle4_other)

    def is_similar(self, other):
        # Проверка на подобие двух четырехугольников
        if not isinstance(other, Descr):
            return False  # Проверка на то, что другой объект также является Descr

        # Получение длин сторон текущего четырехугольника
        a1, b1, c1, d1 = self.get_side_lengths()
        # Получение длин сторон другого четырехугольника
        a2, b2, c2, d2 = other.get_side_lengths()
        # Получение первого угла текущего четырехугольника
        angle1, _, _, _ = self.get_angles()  # Используем только первый угол
        # Получение первого угла другого четырехугольника
        angle2, _, _, _ = other.get_angles()  # Используем только первый угол

        # Проверка на пропорциональность сторон и равенство углов
        return (a1 / a2 == b1 / b2 == c1 / c2 == d1 / d2) and (angle1 == angle2)

    def get_vertices(self):
        # Запрашивает у пользователя координаты четырехугольника
        print("Введите координаты четырех вершин четырехугольника:")
        x1 = float(input("Введите x1: "))
        y1 = float(input("Введите y1: "))
        x2 = float(input("Введите x2: "))
        y2 = float(input("Введите y2: "))

        x3 = float(input("Введите x3: "))
        y3 = float(input("Введите y3: "))
        x4 = float(input("Введите x4: "))
        y4 = float(input("Введите y4: "))
        # Возвращает координаты вершин в виде кортежа
        return ((x1, y1), (x2, y2), (x3, y3), (x4, y4))

    def get_side_length(self, index1, index2):
        # Вычисляет длину стороны между двумя вершинами, заданными индексами
        x1, y1 = self.vertices[index1]
        x2, y2 = self.vertices[index2]
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # Использует теорему Пифагора

    def get_side_lengths(self):
        # Получает длины всех сторон четырехугольника
        a = self.get_side_length(0, 1)  # длина стороны AB
        b = self.get_side_length(1, 2)  # длина стороны BC
        c = self.get_side_length(2, 3)  # длина стороны CD
        d = self.get_side_length(3, 0)  # длина стороны DA
        return a, b, c, d

    def get_angle(self, a, b, c):
        """
        Вычисляет угол между сторонами длиной a, b и c.
        Формула: угол = acos((a^2 + b^2 - c^2) / (2 * a * b))
        Возвращает угол в градусах.
        """
        return acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)) * 180 / pi

    def get_angles(self):
        # Получает углы четырехугольника, используя длины всех сторон
        a, b, c, d = self.get_side_lengths()
        angle1 = self.get_angle(a, b, c)  # угол ABC
        angle2 = self.get_angle(b, c, d)  # угол BCD
        angle3 = self.get_angle(c, d, a)  # угол CDA
        angle4 = self.get_angle(d, a, b)  # угол DAB
        return angle1, angle2, angle3, angle4

# Создаем объект quad1 и запрашиваем у пользователя координаты
quad1 = Descr()
print("Введенный четырехугольник:", quad1)

# Создаем объект quad2 и запрашиваем у пользователя координаты
quad2 = Descr()
print("Введенный четырехугольник:", quad2)

# Сравниваем два четырехугольника на равенство
print("Четырехугольники равны?", quad1 == quad2)

# Проверяем, являются ли четыреугольники подобными
print("Четырехугольники подобны?", quad1.is_similar(quad2))
