import math

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def r(self):
        return math.sqrt(self._x ** 2 + self._y ** 2)

    @r.setter
    def r(self, value):
        angle = self.a
        self._x = value * math.cos(angle)
        self._y = value * math.sin(angle)

    @property
    def a(self):
        return math.atan2(self._y, self._x)

    @a.setter
    def a(self, value):
        radius = self.r
        self._x = radius * math.cos(value)
        self._y = radius * math.sin(value)