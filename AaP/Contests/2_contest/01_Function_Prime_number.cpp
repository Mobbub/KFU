#include <iostream>
#include <cmath>

int is_prime(int number) {
    int b = 0;
    for (int i = 1; i <= sqrt(number); i++) {
        if (number % i == 0) {
            b++;
        }
    }
    if (b > 1) {
        return false;
    }
    return true;
}
