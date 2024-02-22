#include <iostream>
#include <map>

using namespace std;

int main() {
    int n;
    cin >> n;
    string temp;
    int max = 0;
    map<string, int> ymap;
    for (int i = 0; i < n; i++) {
        cin >> temp;
        ymap[temp] += 1;
    }
    for (const auto& element : ymap) {
        if (element.second > max) {
            max = element.second;
        }
    }
    for (const auto& element : ymap) {
        if (element.second == max) {
            cout << element.first << " ";
        }
    }
}
