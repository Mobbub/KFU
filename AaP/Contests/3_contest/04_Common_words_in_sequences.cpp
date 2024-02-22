#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

int main()
{
    int a;
    cin >> a;
    vector<string> x(a);
    for (int i = 0; i < a; i++) {
        cin >> x[i];
    }
    int b;
    cin >> b;
    vector<string> y(b);
    for (int i = 0; i < b; i++) {
        cin >> y[i];
    }
    sort(x.begin(), x.end());
    sort(y.begin(), y.end());
    vector<string> xy;
    set_intersection(x.begin(), x.end(), y.begin(), y.end(), back_inserter(xy));
    for (int i = 1; i < size(xy);i++) {
        if (xy[i] == xy[i - 1]) {
            xy.erase(xy.begin() + i);
        }
    }
    if (xy.empty()) {
        cout << -1;
    }
    else
    {
        for (int i = 0; i < size(xy); i++) {
            cout << xy[i] << " ";
        }
    }
}
