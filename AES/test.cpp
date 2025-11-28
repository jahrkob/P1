#include <math.h>
#include <bitset>
#include <iostream>

using namespace std;

// bitsets have index 0 at the least significant bit

double logTo(int a);

int main() {
    // int a = 21;
    // bitset<8> valueByte = a;
    // cout << valueByte << '\n';
    // for (int i = 0; i < 8; i++) {
    //     cout << valueByte[i] << i << '\n';
    // }
    // return 0;

    cout << logTo(2) << '\n';
    cout << logTo(4) << '\n';
    cout << logTo(8) << '\n';
    cout << logTo(16) << '\n';
    cout << logTo(32) << '\n';
    cout << logTo(64) << '\n';
    cout << logTo(128) << '\n';
    cout << logTo(255) << '\n';
    cout << logTo(256) << '\n';

}


double logTo(int a) {
    return log(a)/log(2);
}