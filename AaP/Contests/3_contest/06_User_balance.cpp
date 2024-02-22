#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>


using namespace std;

int main() {
	int length1, length2, balance;
	string login;
	cin >> length1;
	map<string, int> user;
	for (int i = 0; i < length1; i++) {
		getline(cin, login, ';');
		cin >> balance;
		login.replace(0, 1, "");
		user[login] = balance;
	}
	cin >> length2;
	vector<string> user2(length2);
	for (int i = 0; i < length2; i++) {
		cin >> user2[i];
	}
	for (auto i : user2) {
		cout << user[i] << " ";
	}
}
