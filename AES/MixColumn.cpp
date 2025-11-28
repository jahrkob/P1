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
    if (testModPoly()) {std::cout << "modPoly tests passed" << '\n';} else {throw std::invalid_argument("modPoly tests failed");}
    if (testGF()) { std::cout << "GF2_8 tests passed" << '\n';} else {throw std::invalid_argument("GF2_8 tests failed");}
    if (testMixCol()) {std::cout<<"mixCol tests passed" << '\n';} else {throw std::invalid_argument("mixCol tests failed");}
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
        std::cout << "modPoly(259) did not yield result of 24" << '\n';
    } else if (!(modPoly(0b1000110110) == 0)) {
        std::cout <<  "modPoly(566) did not yield result of 0" << '\n';
    } else if (!(modPoly(0b10001101101) == 1)) {
        std::cout <<  "modPoly(1133) did not yield result of 1" << '\n';
    } else if (!(modPoly(0b111011011) == 192)) {
        std::cout <<  "modPoly(259) did not yield result of 192" << '\n';
    } else {
        return true;
    }
    return false;
}

bool testGF() {
    // test multiplication
    if (!(GFmul(0b10100101,0b110) == 0b11110011)) {
        std::cout << "GF2_8(165) * GF2_8(6) did not yield result of 243" << '\n';
    } else if (!(GFmul(0b10101010,0b110) == 0b11010001)) {
        std::cout << "GF2_8(170) * GF2_8(6) did not yield result of 209" << '\n';
    } else if (!(GFmul(0b10111010,0b110) == 0b10110001)) {
        std::cout << "GF2_8(186) * GF2_8(6) did not yield result of 177" << '\n';
    } 

    // test +/-
    else if (!(GFadd(0b10111010,0b11111010) == 0b01000000)) {
        std::cout << "GF2_8(0b10111010) + GF2_8(0b11111010) did not yield result of 0b01000000" << '\n';
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
    return returnValue;
}
