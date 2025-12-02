
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

uint8_t subBytesTable[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};

/// @brief GF(2^8) addition of a and b
int GFadd(int a, int b, int c=0, int d=0) {
    return modPoly(a ^ b ^ c ^ d);
}

/// @brief GF(2^8) multiplication of a and bz
int GFmul(int a, int b) {
    int curSum = 0;
    for (int bitIndex = 0; bitIndex < 8; bitIndex++) {
        curSum ^= (a*bitRead(b,bitIndex))<<bitIndex; // note if valueByte[index] is 0 nothing gets xor'ed
    };
    return modPoly(curSum);
}

void AESMixCol(uint8_t inOut[16]) {
    uint8_t temp[16];
    for (int i = 0; i < 16; i++) {
        temp[i] = inOut[i];
    }

    inOut[0] = GFadd(GFmul(temp[0],2)   ,GFmul(temp[1],3)    ,temp[2]             ,temp[3]);
    inOut[1] = GFadd(temp[0]            ,GFmul(temp[1],2)    ,GFmul(temp[2],3)    ,temp[3]);
    inOut[2] = GFadd(temp[0]            ,temp[1]             ,GFmul(temp[2],2)    ,GFmul(temp[3],3));
    inOut[3] = GFadd(GFmul(temp[0],3)   ,temp[1]             ,temp[2]             ,GFmul(temp[3],2));

    inOut[4] = GFadd(GFmul(temp[4],2)   ,GFmul(temp[5],3)    ,temp[6]             ,temp[7]);
    inOut[5] = GFadd(temp[4]            ,GFmul(temp[5],2)    ,GFmul(temp[6],3)    ,temp[7]);
    inOut[6] = GFadd(temp[4]            ,temp[5]             ,GFmul(temp[6],2)    ,GFmul(temp[7],3));
    inOut[7] = GFadd(GFmul(temp[4],3)   ,temp[5]             ,temp[6]             ,GFmul(temp[7],2));

    inOut[8] = GFadd(GFmul(temp[8],2)   ,GFmul(temp[9],3)    ,temp[10]             ,temp[11]);
    inOut[9] = GFadd(temp[8]            ,GFmul(temp[9],2)    ,GFmul(temp[10],3)    ,temp[11]);
    inOut[10] = GFadd(temp[8]           ,temp[9]             ,GFmul(temp[10],2)    ,GFmul(temp[11],3));
    inOut[11] = GFadd(GFmul(temp[8],3)  ,temp[9]             ,temp[10]             ,GFmul(temp[11],2));

    inOut[12] = GFadd(GFmul(temp[12],2)  ,GFmul(temp[13],3)    ,temp[14]             ,temp[15]);
    inOut[13] = GFadd(temp[12]           ,GFmul(temp[13],2)    ,GFmul(temp[14],3)    ,temp[15]);
    inOut[14] = GFadd(temp[12]           ,temp[13]             ,GFmul(temp[14],2)    ,GFmul(temp[15],3));
    inOut[15] = GFadd(GFmul(temp[12],3)  ,temp[13]             ,temp[14]             ,GFmul(temp[15],2));
}

void AESShiftRow(uint8_t inOut[16]) {
    uint8_t temp[16];
    for (int i = 0; i < 16; i++){
        temp[i] = inOut[i];
    }
    inOut[0]=temp[0];   inOut[1]=temp[5];   inOut[2]=temp[10];  inOut[3]=temp[15];
    inOut[4]=temp[4];   inOut[5]=temp[9];   inOut[6]=temp[14];  inOut[7]=temp[3];
    inOut[8]=temp[8];   inOut[9]=temp[13];  inOut[10]=temp[2];  inOut[11]=temp[7];
    inOut[12]=temp[12]; inOut[13]=temp[1];  inOut[14]=temp[6];  inOut[15]=temp[11];
}

void AESSubBytes(uint8_t inOut[16]) {
    for (int i = 0; i < 16; i++) {
        inOut[i] = subBytesTable[inOut[i]];
    }
}


void AESAddKey(uint8_t inOut[16], uint8_t key[16]) {
    for (int i = 0; i < 16; i++) {
        inOut[i] = inOut[i] ^ key[i];
    }
}

void g(uint8_t ptrPrevLastWord[4], uint8_t out[4],uint8_t constant) {
    uint8_t subBytes[4];
    for(int i = 0; i < 4; i++) { // starts at 1 eneds at 4 to shift left without shifting left
        subBytes[i] = subBytesTable[int(ptrPrevLastWord[(i+1)%4])]; // Substitute each byte
    }
    subBytes[0] ^= constant;
    for(int i = 0; i < 4; i++) {
        out[i] = subBytes[i];
    }
}

void AESKeyExpansion(uint8_t key[16], uint8_t out[176]) {
    uint8_t RC[10] = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36};
    for(int i = 0; i < 16; i++) {
        // add the initial key to the output list
        out[i] = key[i];
    }
    for(int i = 0; i < 10; i++) {
        uint8_t *prevWords = &out[i*16]; // get reference to previous words start value
        g(&prevWords[12],&out[i*16+16],RC[i]);
        for(int j = 0; j < 4; j++) {
            out[i*16+16+j] ^= out[i*16+j]; // first word of new key (w_5 = w_1 ^ g_val) from python
        }
        for(int j = 0; j < 12; j++) {
            out[i*16+20+j] = out[i*16+4+j] ^ out[i*16+16+j]; // (w_6 = w_2 ^ w_5) (w_7 = w_3 ^ w_6) (w_8 = w_4 ^ w_7)
        }
    }
}

void splitIntoChunks() {
    Serial.println("I would rather kms than write this :C");
}

void AES(uint8_t in[16], uint8_t out[16], uint8_t key[16]) {
    uint8_t keys[176];
    AESKeyExpansion(key,keys);
    uint8_t temp[16];
    for(int i = 0; i < 16; i++) {
        temp[i] = in[i];
    }
    
    for(int i = 0; i < 11; i++) {
        if (i == 0) {
            AESAddKey(temp,keys[i]);
            continue;
        }
        AESSubBytes(temp);
        AESShiftRow(temp);
        if (round != 10) {
            AESMixCol(temp);
        }
        AESAddKey(temp,key);
    }
    for(int i = 0; i < 16; i++) {
        Serial.println(temp[i], HEX);
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////   main   //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////

int mainFromCpp() {
    // the things below are doctests
    if (testModPoly()) {Serial.println("modPoly passed tests");} else {Serial.println("modPoly tests failed");}
    if (testGF()) {Serial.println("GF2_8 passed tests");} else {Serial.println("GF2_8 tests failed");}
    testAESMixCol();
    testAESShiftRow();
    testAESSubBytes();
    testAESAddKey();
    testgFunc();
    testAESKeyExpansion();
    uint8_t out[16];
    AES(0x9a21a2fd8aa9c0fa66a354d9d0184b598e64ce873f174dbb2423fcd814580e15, out, 0x6162636465666768696a6b6c6d6e6f70);
}

void setup() {
  Serial.begin(2000000);
  Serial.println();
  mainFromCpp();
}

void loop() {
  delay(200);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////  TESTING  /////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////


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

bool testAESMixCol() {
    uint8_t inOut[16] =  {0x63, 0x2f, 0xaf, 0xa2, 0xeb, 0x93, 0xc7, 0x20, 0x9f, 0x92, 0xab, 0xcb, 0xa0, 0xc0, 0x30, 0x2b};
    int lenOut;
    int lenExpected;
    uint8_t expectedOut[16] = {0xba, 0x75, 0xf4, 0x7a, 0x84, 0xa4, 0x8d, 0x32, 0xe8, 0x8d, 0x06, 0x0e, 0x1b, 0x40, 0x7d, 0x5d};
    AESMixCol(inOut);
    for (int i = 0; i < 16; i++) {
        if (inOut[i] != expectedOut[i]) {
            Serial.println("FAILED: AESMixCol tests failed");
            Serial.print(inOut[i]);
            Serial.print(" - ");
            Serial.println(expectedOut[i]);
            return false;
        }
    }
    Serial.println("AESMixCol passed tests");
    return true;
}

bool testAESShiftRow() {
    uint8_t inOut[16] = {0x63, 0xc0, 0xab, 0x20, 0xeb, 0x2f, 0x30, 0xcb, 0x9f, 0x93, 0xaf, 0x2b, 0xa0, 0x92, 0xc7, 0xa2};
    uint8_t expected[16] = {0x63, 0x2f, 0xaf, 0xa2, 0xeb, 0x93, 0xc7, 0x20, 0x9f, 0x92, 0xab, 0xcb, 0xa0, 0xc0, 0x30, 0x2b};
    AESShiftRow(inOut);
    bool returnValue = true;
    for (int i = 0; i < 16; i++) {
        //Serial.print(inOut[i]);
        //Serial.print(" - ");
        //Serial.print(expected[i]);
        if (inOut[i] != expected[i] && returnValue) {
            Serial.println("\nFAILED: AESShiftRow failed tests");
            returnValue = false;
        } else {
            //Serial.print('\n');
        }
    }
    if (returnValue) {
        Serial.println("AESShiftrow passed tests");
    }
    return true;
}

bool testAESSubBytes() {
    uint8_t inOut[16] = {0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef, 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef};
    uint8_t expected[16] = {0x7c, 0x26, 0x6e, 0x85, 0xa7, 0x62, 0xbd, 0xdf, 0x7c, 0x26, 0x6e, 0x85, 0xa7, 0x62, 0xbd, 0xdf};
    AESSubBytes(inOut);
    bool returnValue = true;
    for (int i = 0; i < 16; i++) {
        //Serial.print(inOut[i]);
        //Serial.print(" - ");
        //Serial.print(expected[i]);
        if (inOut[i] != expected[i] && returnValue) {
            Serial.println("\nFAILED: AESSubBytes failed tests");
            returnValue = false;
        } else {
            //Serial.print('\n');
        }
    }
    if (returnValue) {
        Serial.println("AESSubBytes passed tests");
    }
    return true;
}

bool testAESAddKey() {
    uint8_t inOut[16] = {
        0x54, 0x77, 0x6f, 0x20,
        0x4f, 0x6e, 0x65, 0x20,
        0x4e, 0x69, 0x6e, 0x65,
        0x20, 0x54, 0x77, 0x6f
    };
    uint8_t key[16] = {
        0x54, 0x68, 0x61, 0x74,
        0x73, 0x20, 0x6d, 0x79,
        0x20, 0x4b, 0x75, 0x6e,
        0x67, 0x20, 0x46, 0x75
    };
    uint8_t expected[16] = {
        0x00, 0x1f, 0x0e, 0x54, 
        0x3c, 0x4e, 0x08, 0x59, 
        0x6e, 0x22, 0x1b, 0x0b, 
        0x47, 0x74, 0x31, 0x1a
    };
    AESAddKey(inOut,key);
    bool returnValue = true;
    for (int i = 0; i < 16; i++) {
        //Serial.print(inOut[i]);
        //Serial.print(" - ");
        //Serial.print(expected[i]);
        if (inOut[i] != expected[i] && returnValue) {
            //Serial.println("\nFAILED: AESAddKey failed tests");
            returnValue = false;
        } else {
            //Serial.print('\n');
        }
    }
    if (returnValue) {
        Serial.println("AESAddKey passed tests");
    }
    return true;
}

bool testgFunc() {
    uint8_t in[4] = {0x12,0x34,0x56,0x78};
    uint8_t out[4];
    uint8_t expected[4] = {0x19, 0xb1, 0xbc, 0xc9};
    g(in,out,1);
    bool returnValue = true;
    for (int i = 0; i < 4; i++) {
        //Serial.print(out[i]);
        //Serial.print(" - ");
        //Serial.print(expected[i]);
        if (out[i] != expected[i] && returnValue) {
            Serial.println("\nFAILED: g function failed tests");
            returnValue = false;
        } else {
            //Serial.print('\n');
        }
    }
    if (returnValue) {
        Serial.println("g function passed tests");
    }
    return true;
}

bool testAESKeyExpansion() {
    uint8_t in[16] = {0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6D, 0x79, 0x20, 0x4B, 0x75,0x6E, 0x67, 0x20, 0x46, 0x75};
    uint8_t out[176];
    uint8_t expected[16] = {0xe2, 0x32, 0xfc, 0xf1, 0x91, 0x12, 0x91, 0x88, 0xb1, 0x59, 0xe4, 0xe6, 0xd6, 0x79, 0xa2, 0x93};
    uint8_t expected2[16] = {0x56, 0x08, 0x20, 0x07, 0xc7, 0x1a, 0xb1, 0x8f, 0x76, 0x43, 0x55, 0x69, 0xa0,0x3a, 0xf7, 0xfa};
    AESKeyExpansion(in,out);
    bool returnValue = true;
    for (int i = 0; i < 16; i++) {
        //Serial.print(out[i+16]);
        //Serial.print(" - ");
        //Serial.print(expected[i]);
        if (out[i+16] != expected[i] && returnValue) {
            Serial.println("\nFAILED: AESKeyExpansion failed tests");
            returnValue = false;
        } else {
            //Serial.print('\n');
        }
    }
    ////////// test 2 //////////
    for (int i = 0; i < 16; i++) {
        //Serial.print(out[i+32]);
        //Serial.print(" - ");
        //Serial.print(expected2[i]);
        if (out[i+32] != expected2[i] && returnValue) {
            Serial.println("\nFAILED: AESKeyExpansion failed tests");
            returnValue = false;
        } else {
            //Serial.print('\n');
        }
    }

    if (returnValue) {
        Serial.println("AESKeyExpansion passed tests");
    }
    return true;
}