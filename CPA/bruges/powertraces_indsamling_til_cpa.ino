#include <AESLib.h>

AES aes;

byte aes_key[16] = {
  0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,
  0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x10
};

byte plaintext[16] = {
  0xde,0xad,0x00,0xbe,0xef,0x00,0xca,0xfe,
  0xde,0xad,0x00,0xbe,0xef,0x00,0xca,0xfe
};

byte ciphertext[32];

const int triggerPin = 2;

void setup() {
  Serial.begin(115200);

  pinMode(triggerPin, OUTPUT);
  digitalWrite(triggerPin, LOW);

  // Seed så plaintext kan ændre sig
  randomSeed(analogRead(A0));
}

void loop() {
  // --- NYT: ændr plaintext pr. trace ---
  for (int i = 0; i < 16; i++) {
    plaintext[i] = (byte)random(0, 256);
  }

  // Trigger HIGH før kryptering (scope alignment)
  digitalWrite(triggerPin, HIGH);

  aes.set_key(aes_key, 16);
  aes.encrypt(plaintext, ciphertext);

  // Trigger LOW efter kryptering
  digitalWrite(triggerPin, LOW);

  // (valgfrit men stærkt anbefalet)
  // Print plaintext i hex så du kan gemme den pr. trace
  for (int i = 0; i < 16; i++) {
    if (plaintext[i] < 16) Serial.print('0');
    Serial.print(plaintext[i], HEX);
  }
  Serial.println();
}
