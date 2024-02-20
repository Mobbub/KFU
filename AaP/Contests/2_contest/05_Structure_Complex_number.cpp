#include <iostream>
using namespace std;

Complex make_complex(string number)
{
unsigned long long biggest_number = 18446744073709551615;
while (number.find(' ') != biggest_number)
    {
        number.replace(number.find(' '), 1, "");
    }
    string num1 = "";
    string num2 = "";
    int iterator = 1;
    num1 += number[0];
    while (number[iterator] != '+' && number[iterator] != '-')
    {
        num1 += number[iterator];
        iterator++;
    }
    while (iterator < number.length())
    {
        num2 += number[iterator];
        iterator++;
    }
    Complex result;
    result.re = stod(num1);
    result.im = stod(num2);
    return result;
}


Complex sum(Complex c1, Complex c2)
{
    Complex result;
    result.re = c1.re + c2.re;
    result.im = c1.im + c2.im;
    return result;
}

Complex sub(Complex c1, Complex c2)
{
    Complex result;
    result.re = c1.re - c2.re;
    result.im = c1.im - c2.im;
    return result;
}

Complex mul(Complex c1, Complex c2)
{
    Complex result;
    result.re = c1.re * c2.re - c1.im * c2.im;
    result.im = c1.im * c2.re + c2.im * c1.re;
    return result;
}

Complex div(Complex c1, Complex c2)
{
    Complex result;
    double denominator = c2.re * c2.re + c2.im * c2.im;
    result.re = (c1.re * c2.re + c1.im * c2.im) / denominator;
    result.im = (c1.im * c2.re - c1.re * c2.im) / denominator;
    return result;
}

void print(Complex number)
{
    cout << number.re;
    if (number.im == 0) number.im = 0;
    if (number.im >= 0) cout << '+';
    cout << number.im;
    cout << 'j' << endl;
}
