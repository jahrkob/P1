#include <Arduino.h>
#include <math.h>

int modPoly(int poly);

/// @brief GF(2^8) addition of a and b
int GFadd(int a, int b, int c=0, int d=0) {
    return modPoly(a ^ b ^ c ^ d);
}

/// @brief GF(2^8) multiplication of a and b
int GFmul(int a, int b) {
    int curSum = 0;
    for (int bitIndex = 0; bitIndex < 8; bitIndex++) {
        curSum ^= (a*bitRead(b,bitIndex))<<bitIndex; // note if valueByte[index] is 0 nothing gets xor'ed
    };
    return modPoly(curSum);
}

/// @brief Does the mix column function for a column
/// @param col The column to mix
/// @param out The array which will be edditted to hold the return value of mix col
void mixCol(int col[4], int out[4]) {
  out[0] = GFadd(GFmul(col[0],2)   ,GFmul(col[1],3)    ,col[2]             ,col[3]);
  out[1] = GFadd(col[0]            ,GFmul(col[1],2)    ,GFmul(col[2],3)    ,col[3]);
  out[2] = GFadd(col[0]            ,col[1]             ,GFmul(col[2],2)    ,GFmul(col[3],3));
  out[3] = GFadd(GFmul(col[0],3)   ,col[1]             ,col[2]             ,GFmul(col[3],2));
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int mainFromCpp() {
    // the things below are doctests
    if (testModPoly()) {Serial.println("modPoly tests passed");} else {Serial.println("modPoly tests failed");}
    if (testGF()) {Serial.println("GF2_8 tests passed");} else {Serial.println("GF2_8 tests failed");}
    if (testMixCol()) {Serial.println("mixCol tests passed");} else {Serial.println("mixCol tests failed");}
    int list[] = {1,2,3,4};
    int mixedCol[4];
    mixCol(list,mixedCol);
    Serial.println(mixedCol[0]);
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
        Serial.println("modPoly(259) did not yield result of 24");
    } else if (!(modPoly(0b1000110110) == 0)) {
        Serial.println( "modPoly(566) did not yield result of 0");
    } else if (!(modPoly(0b10001101101) == 1)) {
        Serial.println( "modPoly(1133) did not yield result of 1");
    } else if (!(modPoly(0b111011011) == 192)) {
        Serial.println( "modPoly(259) did not yield result of 192");
    } else {
        return true;
    }
    return false;
}

bool testGF() {
    // test multiplication
    if (!(GFmul(0b10100101,0b110) == 0b11110011)) {
        Serial.println("GF2_8(165) * GF2_8(6) did not yield result of 243");
    } else if (!(GFmul(0b10101010,0b110) == 0b11010001)) {
        Serial.println("GF2_8(170) * GF2_8(6) did not yield result of 209");
    } else if (!(GFmul(0b10111010,0b110) == 0b10110001)) {
        Serial.println("GF2_8(186) * GF2_8(6) did not yield result of 177");
    } 

    // test +/-
    else if (!(GFadd(0b10111010,0b11111010) == 0b01000000)) {
        Serial.println("GF2_8(0b10111010) + GF2_8(0b11111010) did not yield result of 0b01000000");
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
  int result1[4];
  mixCol(list1,result1);
  int result2[4];
  mixCol(list2,result2);
  bool returnValue = true; // true unless error then we change to false
  for (int i = 0; i < 4; i++) {
      if (result1[i] != desiredResult1[i]) {
          Serial.println("mixCol({1,2,3,4}) did not yield result of {3,4,9,10}");
          returnValue = false;
      }
  }
  for (int i = 0; i < 4; i++) {
    if (result2[i] != desiredResult2[i]) {
        Serial.println("mixCol({0x47,0x37,0x94,0xed}) did not yield result of {0x87, 0x6e, 0x46, 0xa6}");
        returnValue = false;
    }
  }
  return returnValue;
}

////////////////////////////////////////////////////////////////////////////////////////

void setup() {
  Serial.begin(9600);
  mainFromCpp();
}

void loop() {
  delay(200);
}
