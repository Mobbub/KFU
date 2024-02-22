#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> a;
    int b;
    cin >> b;
    for (int i = 0; i < b; i++) {
        int num;
        cin >> num;
        a.push_back(num);
    }
    sort(a.begin(), a.end());
    int b2;
    cin >> b2;
    for (int j = 0; j < b2; j++) {
        int num;
        cin >> num;
        a.push_back(num);
    }
    sort(a.begin(), a.end());
    for (int i = 0; i < a.size(); i++) {
        cout << a[i] << " ";
    }
}
