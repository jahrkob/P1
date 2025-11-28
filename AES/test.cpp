#include <math.h>
#include <bitset>
#include <iostream>

using namespace std;

// bitsets have index 0 at the least significant bit

double logTo(int a);
int* mixCol(int col[]);
int GFmul(int a, int b);
int GFadd(int a, int b);
int modPoly(int poly);

int main() {
    // int a = 21;
    // bitset<8> valueByte = a;
    // cout << valueByte << '\n';
    // for (int i = 0; i < 8; i++) {
    //     cout << valueByte[i] << i << '\n';
    // }
    // return 0;

    // cout << logTo(2) << '\n';
    // cout << logTo(4) << '\n';
    // cout << logTo(8) << '\n';
    // cout << logTo(16) << '\n';
    // cout << logTo(32) << '\n';
    // cout << logTo(64) << '\n';
    // cout << logTo(128) << '\n';
    // cout << logTo(255) << '\n';
    // cout << logTo(256) << '\n';

    // int list1[4] = {1,2,3,4};
    // int list2[4] = {0x47,0x37,0x94,0xed};
    // int result1[4] = {3,4,9,10};
    // int result2[4] = {0x87, 0x6e, 0x46, 0xa6};
    // std::cout << *mixCol(list1) << '\n';
    // std::cout << *mixCol(list2) << '\n';
    
    int list1[4] = {1,2,3,4};
    int list2[4] = {0x47,0x37,0x94,0xed};
    int desiredResult1[4] = {3,4,9,10};
    int desiredResult2[4] = {0x87, 0x6e, 0x46, 0xa6};
    int* result1 = mixCol(list1);
    int* result2 = mixCol(list2);
    bool returnValue = true; // true unless error then we change to false
    for (int i = 0; i < 4; i++) {
        if (result1[i] != desiredResult1[i]) {
            std::cout << "mixCol({1,2,3,4}) did not yield result of {3,4,9,10}" << '\n';
            returnValue = false;
        }
    }
    for (int i = 0; i < 4; i++) {
        if (result2[i] != desiredResult2[i]) {
            std::cout << "mixCol({0x47,0x37,0x94,0xed}) did not yield result of {0x87, 0x6e, 0x46, 0xa6}" << '\n';
            returnValue = false;
        }
    }
}


double logTo(int a) {
    return log(a)/log(2);
}

/// @brief GF(2^8) addition of a and b
int GFadd(int a, int b, int c=0, int d=0) {
    return modPoly(a ^ b ^ c ^ d);
}

/// @brief GF(2^8) multiplication of a and b
int GFmul(int a, int b) {
    int curSum = 0;
    std::bitset<8> valueByte = b; // note that bitsets have index 0 at the least significant bit
    for (int bitIndex = 0; bitIndex < 8; bitIndex++) {
        curSum ^= (a*valueByte[bitIndex])<<bitIndex; // note if valueByte[index] is 0 nothing gets xor'ed
    };
    return modPoly(curSum);
}


int* mixCol(int col[]) {
    int *list = new int[4] {
        GFadd(GFmul(col[0],2)   ,GFmul(col[1],3)    ,col[2]             ,col[3])         ,
        GFadd(col[0]            ,GFmul(col[1],2)    ,GFmul(col[2],3)    ,col[3])         ,
        GFadd(col[0]            ,col[1]             ,GFmul(col[2],2)    ,GFmul(col[3],3)),
        GFadd(GFmul(col[0],3)   ,col[1]             ,col[2]             ,GFmul(col[3],2))
    };
    std::cout << list[0] << '\n';
    std::cout << list[1] << '\n';
    std::cout << list[2] << '\n';
    std::cout << list[3] << '\n';
    return list;
}

/// @brief Functions which makes sure any value fits in GF2_8 by using the AES irreducible polynomial 0b100011011
/// @param poly The value which we want to reduce to fit in GF2_8
/// @return Reduced poly as integer
int modPoly(int poly) {
    while ((poly != 0) && (log10(poly)/log10(2) >= 8)) {
        int shiftBy = floor(logTo(int(poly)))-8;
        poly ^= 0b100011011<<shiftBy; // 0b100011011 is the aes irreducible polynomial
    }
    return poly;
}