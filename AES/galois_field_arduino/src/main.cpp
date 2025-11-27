#include <Arduino.h>
#include <math.h>

// put function declarations here:
struct GF2_8 {
  int value;
  GF2_8(int inputValue)
    : value(inputValue) {}

  GF2_8 operator+(const GF2_8& other) const {
    return GF2_8(value ^ other.value);
  }

  GF2_8 operator-(const GF2_8& other) const {
    // should be exact replica of the '+' operator
    return GF2_8(value ^ other.value);
  }

  GF2_8 operator*(const GF2_8& other) const {
    int curSum = 0;
    byte valueByte = byte(other.value);
    for (int bit = 0; bit < 8; bit++) {
      valueByte[bit];
    };
    return GF2_8(value ^ other.value);
  }

  int integer() const {
    return value;
  }

};

int modPoly(int poly) {
  if (poly == 0) {
    return 0
  } else {
    while (log10(poly)/log10(2) >= 8)
  }
}


void setup() {
  // put your setup code here, to run once:
  int result = myFunction(2, 3);
}

void loop() {
  // put your main code here, to run repeatedly:
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}