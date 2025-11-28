#include <math.h>
#include <bitset>
#include <iostream>

int modPoly(int poly);
double logTo(int a);
bool testModPoly();
bool testGF();

struct GF2_8 {
  int value;
  GF2_8(int inputValue)
    : value(modPoly(inputValue)) {}

  GF2_8 operator+(const GF2_8& other) const {
    return GF2_8(value ^ other.value);
  }

  GF2_8 operator-(const GF2_8& other) const {
    // should be exact replica of the '+' operator
    return GF2_8(value ^ other.value);
  }

  GF2_8 operator*(const GF2_8& other) const {
    int curSum = 0;
    std::bitset<8> valueByte = other.value; // note that bitsets have index 0 at the least significant bit
    for (int bitIndex = 0; bitIndex < 8; bitIndex++) {
        curSum ^= (value*valueByte[bitIndex])<<bitIndex; // note if valueByte[index] is 0 nothing gets xor'ed
    };
    return GF2_8(curSum);
  }

    bool operator==(const int& b) {
        return value == b;
    }

  int operator<<(std::ostream &strm) const {
    return value;
  }

  int integer() const {
    return value;
  }

};

std::ostream& operator<<(std::ostream& os, const GF2_8& obj) {
    return os << obj.value;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main() {
    // the things below are doctests
    if (testModPoly()) {
        std::cout << "modPoly tests passed" << '\n';
    } else {
        throw "modPoly tests failed";
    }
    if (testGF()) {
        std::cout << "GF2_8 tests passed" << '\n';
    } else {
        throw "GF2_8 tests failed";
    }
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
    if (!((GF2_8(0b10100101) * GF2_8(0b110)) == 0b11110011)) {
        throw "GF2_8(165) * GF2_8(6) did not yield result of 243";
    } else if (!((GF2_8(0b10101010) * GF2_8(0b110)) == 0b11010001)) {
        throw "GF2_8(170) * GF2_8(6) did not yield result of 209";
    } else if (!((GF2_8(0b10111010) * GF2_8(0b110)) == 0b10110001)) {
        throw "GF2_8(186) * GF2_8(6) did not yield result of 177";
    } 

    // test +/-
    else if (!((GF2_8(0b10111010) + GF2_8(0b11111010)) == 0b01000000)) {
        throw "GF2_8(0b10111010) + GF2_8(0b11111010) did not yield result of 0b01000000";
    } else if (!((GF2_8(0b10111010) - GF2_8(0b11111010)) == 0b01000000)) {
        throw "GF2_8(0b10111010) - GF2_8(0b11111010) did not yield result of 0b01000000";
    } 
    
    // if no tests failed return true else false
    else {
        return true;
    }
    return false;
}
