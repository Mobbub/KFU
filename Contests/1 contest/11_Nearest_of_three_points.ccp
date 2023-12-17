#include <iostream>
using namespace std;
int main() {
    int a;
    cin >> a;
    int b;
    cin >> b;
    int c;
    cin >> c;
    int a1;
    int a2;
    if(b > a)
    {
        a1 = b - a;
    }
    else
    {
        a1 = a - b;
    }
    if(c > a)
    {
        a2 = c - a;
    }
    else
    {
        a2 = a - c;
    }
    if(a1 < a2)
    {
        cout << 'B' << ' ' << a1;
    }
    else
    {
        cout<< 'C' << ' ' << a2;
    }
}
