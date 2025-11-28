#include <math.h>
#include <bitset>
#include <iostream>

int modPoly(int poly);
double logTo(int a);
bool testModPoly();
bool testGF();
bool testMixCol();

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

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main() {
    // the things below are doctests
    if (testModPoly()) {std::cout << "modPoly tests passed" << '\n';} else {throw "modPoly tests failed";}
    if (testGF()) { std::cout << "GF2_8 tests passed" << '\n';} else {throw "GF2_8 tests failed";}
    if (testMixCol()) {std::cout<<"mixCol tests passed" << '\n';} else {throw "mixCol tests failed";}
    int list[] = {1,2,3,4};
    int* ptr = mixCol(list);
    std::cout << ptr[0];
    delete[] ptr;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/// @brief A log2 function
/// @param a Integer to get log2 of
/// @return Returns the log2 of a
double logTo(int a) {
    return log(a)/log(2);
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



/////////////////////////////////////  TESTING  //////////////////////////////////////////////////////////

/// @brief Tests the modPoly function
/// @return Returns true if tests passed throws exception otherwise
bool testModPoly() {
    if (!(modPoly(0b100000011) == 24)) {
        throw "modPoly(259) did not yield result of 24";
    } else if (!(modPoly(0b1000110110) == 0)) {
        throw "modPoly(566) did not yield result of 0";
    } else if (!(modPoly(0b10001101101) == 1)) {
        throw "modPoly(1133) did not yield result of 1";
    } else if (!(modPoly(0b111011011) == 192)) {
        throw "modPoly(259) did not yield result of 192";
    } else {
        return true;
    }
    return false;
}

bool testGF() {
    // test multiplication
    if (!(GFmul(0b10100101,0b110) == 0b11110011)) {
        throw "GF2_8(165) * GF2_8(6) did not yield result of 243";
    } else if (!(GFmul(0b10101010,0b110) == 0b11010001)) {
        throw "GF2_8(170) * GF2_8(6) did not yield result of 209";
    } else if (!(GFmul(0b10111010,0b110) == 0b10110001)) {
        throw "GF2_8(186) * GF2_8(6) did not yield result of 177";
    } 

    // test +/-
    else if (!(GFadd(0b10111010,0b11111010) == 0b01000000)) {
        throw "GF2_8(0b10111010) + GF2_8(0b11111010) did not yield result of 0b01000000";
    }
    
    // if no tests failed return true else false
    else {
        return true;
    }
    return false;
}

bool testMixCol() {
    int list1[4] = {1,2,3,4};
    int list2[4] = {0x47,0x37,0x94,0xed};
    int result1[4] = {3,4,9,10};
    int result2[4] = {0x87, 0x6e, 0x46, 0xa6};
    if (!(mixCol(list1) == result1)) {
        throw "mixCol({1,2,3,4}) did not yield result of {3,4,9,10}";
    } else if (!(mixCol(list2) == result2)) {
        throw "mixCol({0x47,0x37,0x94,0xed}) did not yield result of {0x87, 0x6e, 0x46, 0xa6}";
    } else {
        return true;
    }
    return false;
}
