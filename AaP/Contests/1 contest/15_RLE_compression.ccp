#include <iostream>
#include <string>
using namespace std;
int main() {
    string a;
    cin >> a;
    string c;
    int b = 1;
    for (int i = 0; i < a.length(); ++i) {
        if (a[i] == a[i+1]) {
            ++b;
        }
        else {
            c.push_back(a[i]);
            if (b > 1) {
                c += to_string(b);
                b = 1;
            }
        }
    }
    cout << c;
}
