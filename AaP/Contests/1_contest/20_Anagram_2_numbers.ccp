#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    string input;
    getline(cin, input);
    vector<string> a;
    string temp;
    for (char c : input) {
        if (c == ' ') {
            a.push_back(temp);
            temp = "";
        } else {
            temp += c;
        }
    }
    a.push_back(temp);
    string a1 = a[0];
    string a2 = a[1];
    vector<int> b1;
    vector<int> b2;
    for (int i = 0; i < a1.length(); i++) {
        b1.push_back(a1[i] - '0');
        b2.push_back(a2[i] - '0');
    }
    sort(b1.begin(), b1.end());
    sort(b2.begin(), b2.end());
    if (b1 == b2) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }
    return 0;
}
