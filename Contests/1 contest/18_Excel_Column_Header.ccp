#include <iostream>
#include <string>
using namespace std;
int main() {
    int a;
    cin >> a;
    string b = "";
    while (a > 0) {
        int c = (a - 1) % 26;
        b = char(c + 'A') + b;
        a = (a - 1) / 26;
    }
    cout << b;
}
