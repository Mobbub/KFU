class Water:
    def __init__(self, temperature):
        self.temperature = temperature

    def heat_up(self, degrees):
        self.temperature += degrees

    def is_boiling(self):
        return self.temperature >= 100

class Teapot:
    def __init__(self, water):
        self.water = water

    def heat_up(self, degrees):
        self.water.heat_up(degrees)

    def is_boiling(self):
        return self.water.is_boiling()