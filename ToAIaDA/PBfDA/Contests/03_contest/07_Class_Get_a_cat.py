import random

class Cat:
    def __init__(self, alive):
        self._alive = alive

    def is_alive(self):
        return self._alive

class Box:
    def __init__(self):
        self._cat = None

    def open(self):
        if self._cat is None:
            self._cat = Cat(random.choice([True, False]))
        return self._cat