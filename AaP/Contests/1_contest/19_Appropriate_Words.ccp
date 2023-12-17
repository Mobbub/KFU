#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_set>
using namespace std;
int main() {
    string input;
    getline(cin, input);
    vector<string> a2;
    string word;
    for (char c : input) {
        if (c == ' ') {
            a2.push_back(word);
            word = "";
        } else {
            word += c;
        }
    }
    a2.push_back(word);
    vector<string> a;
    vector<string> a1;
    int b = 1;
    for (int j = 0; j < a2.size(); j++) {
        if (a2[j] != "end") {
            a.push_back(a2[j]);
        } else {
            break;
        }
    }
    for (int i = 0; i < a.size() - 1; i++) {
        int count = 0;
        for (int j = 0; j < a.size(); j++) {
            if (a[i] == a[j]) {
                count++;
            }
        }
        if (count > 1) {
            a1.push_back(a[i]);
        }
    }
    unordered_set<string> k(a1.begin(), a1.end());
    vector<string> sorted_k(k.begin(), k.end());
    sort(sorted_k.begin(), sorted_k.end());
    for (int i = 0; i < sorted_k.size(); i++) {
        cout << sorted_k[i] << " ";
    }
    return 0;
}
