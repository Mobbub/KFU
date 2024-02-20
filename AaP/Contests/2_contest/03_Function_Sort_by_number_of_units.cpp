#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
using namespace std;

int count_ones(string num)
{
    return count(num.begin(), num.end(), '1');
}
bool compare(string a, string b)
{
    int count_a = count_ones(a);
    int count_b = count_ones(b);
    if (count_a == count_b)
    {
        if (stoi(a) < stoi(b))
        {
            return true;
        }
        if (stoi(a) > stoi(b))
        {
            return false;
        }
    }
    else
    {
        if (count_a > count_b)
        {
            return true;
        }
        if (count_a < count_b)
        {
            return false;
        }
    }
}
