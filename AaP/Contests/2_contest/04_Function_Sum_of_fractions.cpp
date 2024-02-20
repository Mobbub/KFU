#include <iostream>
#include <tuple>
using namespace std;

tuple<int, int> reduce(int m, int n) 
{
    if (m == n)
    {
        return tuple<int, int>(1, 1);
    }
    int pointer = min(abs(m), abs(n));
    while (pointer != 0)
    {
        if (m % 2 == 0 && n % 2 == 0)
        {
            m /= 2;
            n /= 2;
            continue;
        }
        if (m % pointer == 0 && n % pointer == 0)
        {
            m /= pointer;
            n /= pointer;
        }
        pointer--;
    }
    return tuple<int, int>(m, n);
}

tuple<int, int, int> find_lcm(int num1, int num2)
{
    int lcm = min(num1, num2);
    if (num1 == num2)
    {
        return tuple<int, int, int>(num1, lcm / num1, lcm / num2);
    }
    while (lcm % max(num1, num2) != 0) 
    {
        lcm += min(num1, num2);
    }
    int c1 = lcm / num1;
    int c2 = lcm / num2;
    return tuple<int, int, int>(lcm, c1, c2);
}
