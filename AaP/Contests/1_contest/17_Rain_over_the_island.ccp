#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    int blocks[n];
    for (int i=0; i<n; i++) {
        cin >> blocks[i];
    }
    u_long water = 0;
    int left = 0;
    int right = n-1;
    int max_left = blocks[left];
    int max_right = blocks[right];
    while (left < right) {
        if (max_left >= max_right) {
            water = water + max_right - blocks[right];
            right--;
            max_right = max(max_right, blocks[right]);
        } 
        else {
            water = water + max_left - blocks[left];
            left++;
            max_left = max(max_left, blocks[left]);
        }
    }
    cout << water;
}
