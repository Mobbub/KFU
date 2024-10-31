class Employee:
    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary

    def bonus(self, percent):
        return round(self.salary * percent)

    def total_salary(self):
        return self.salary + self.bonus(bonuses[self.position])

    def __repr__(self):
        return f"{self.name} ({self.position}): {self.total_salary()}"

class Manager(Employee):
    def __init__(self, name, salary=16242):
        super().__init__(name, 'manager', salary)

    def bonus(self, percent):
        return round(self.salary * max(percent, 0.1))