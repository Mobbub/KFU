#include <iostream>
#include <cmath>
using namespace std;
int main() {
    cout << sqrt(12.0) * (1.0 - (1.0 / 9.0) + (1.0 / (5.0 * 9.0)) - (1.0 / (7.0 * pow(3.0, 3.0))) + (1.0 / (9.0 * pow(3.0, 4.0))) - (1.0 / (11.0 * pow(3.0, 5.0))));
    return 0;
} 
