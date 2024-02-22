#include <iostream>
#include <stack>
#include <string>

using namespace std;

bool isValid(string text) {
    stack<char> brackets;
    for (char c : text) {
        if (c == '(' || c == '{' || c == '[') {
            brackets.push(c);
        } else if (c == ')' || c == '}' || c == ']') {
            if (brackets.empty()) {
                return false;
            }
            char top = brackets.top();
            brackets.pop();
            if ((c == ')' && top != '(') || (c == '}' && top != '{') || (c == ']' && top != '[')) {
                return false;
            }
        }
    }
    return brackets.empty();
}

int main() {
    string text;
    getline(cin, text, '!');
    if (isValid(text)) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }
}
