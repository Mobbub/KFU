#include <cmath>

class Employee 
{
protected:
    std::string _name;
    std::string _position;
    int _base_salary;
    int _bonus_salary;
public:
    Employee(std::string name, std::string position, int salary) 
    {
        this->_name = name;
        this->_position = position;
        this->_base_salary = salary;
        this->_bonus_salary = 0;
    }
    virtual int bonus(double percentage) 
    {
        _bonus_salary = round(_base_salary * percentage);
        return _bonus_salary;
    }
    int salary() 
    {
        bonus(bonuses[_position]);
        return _base_salary + _bonus_salary;
    }
    friend std::ostream& operator<<(std::ostream& os, Employee& employee)
    {
        os << employee._name << " (" << employee._position << "): " << employee.salary();
        return os;
    }
};

class Manager : public Employee 
{
public:
    Manager(std::string name, int salary = 16242) : Employee(name, "manager", salary) {}
    int bonus(double percentage) 
    {
        if (percentage < 0.1)
        {
            percentage = 0.1;
            _bonus_salary = round(_base_salary * percentage);
            return _bonus_salary;
        }
        else
        {
            _bonus_salary = round(_base_salary * percentage);
            return _bonus_salary;
        }
    }
};
