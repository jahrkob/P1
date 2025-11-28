#include <DES.h>

DES des;

const int TRIGGER_PIN = 2;  // Trigger pin for oscilloscope

void setup() {
  Serial.begin(9600);
  Serial.println("Hello!");
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, LOW); // Ensure trigger starts LOW
}

void loop() {
  desTest();
  delay(2000);
}

void desTest() {
  byte out[8];
  byte in[] = { 1, 2, 3, 4, 5, 6, 7, 8 };
  byte key[] = { 0x3b, 0x38, 0x98, 0x37, 0x15, 0x20, 0xf7, 0x5e };

  Serial.println();
  Serial.println("========= DES test ==========");

  // Trigger HIGH before encryption
  digitalWrite(TRIGGER_PIN, HIGH);

  // Encrypt
  Serial.print("Encrypt...");
  unsigned long time = micros();
  des.encrypt(out, in, key);
  time = micros() - time;
  Serial.print("done. (");
  Serial.print(time);
  Serial.println(" micros)");
  printArray(out);

  // Trigger LOW after encryption
  digitalWrite(TRIGGER_PIN, LOW);

  /*
  // ================================
  // Decryption is COMMENTED OUT
  // ================================
  
  for (int i = 0; i < 8; i++) {
    in[i] = out[i];
  }
  Serial.print("Decrypt...");
  time = micros();
  des.decrypt(out, in, key);
  time = micros() - time;
  Serial.print("done. (");
  Serial.print(time);
  Serial.println(" micros)");
  printArray(out);
  */
}

void printArray(byte output[]) {
  for (int i = 0; i < 8; i++) {
    if (output[i] < 0x10) {
      Serial.print("0");
    }
    Serial.print(output[i], HEX);
    Serial.print(" ");
  }
  Serial.println();
}
