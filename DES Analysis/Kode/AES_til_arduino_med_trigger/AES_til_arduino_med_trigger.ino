#include <AES.h>

AES aes;

// Pre-shared key (PSK) - 16 bytes (128 bits)
byte aes_key[16] = {
  0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
  0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10
};

// Initialization Vector (IV) - 16 bytes
byte aes_iv[16] = {
  0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
  0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF
};
byte aes_iv_enc[16];
byte aes_iv_dec[16];

// Trigger pin
const int triggerPin = 2;

void setup() {
  Serial.begin(115200);
  memcpy(aes_iv_enc,aes_iv,16);
  memcpy(aes_iv_dec,aes_iv,16);

  // Setup trigger pin
  pinMode(triggerPin, OUTPUT);
  digitalWrite(triggerPin, LOW);

  // Plaintext message
  const char *plaintext = "Hello, ESP32 AES";
  size_t plaintext_len = strlen(plaintext);

  // Buffer for ciphertext (same size as plaintext)
  byte ciphertext[32];
  // Buffer for decrypted text
  byte decrypted[32];

  Serial.println("=== AES Encryption and Decryption Example ===");

  // ---- Trigger HIGH før kryptering ----
  digitalWrite(triggerPin, HIGH);

  // Encrypt the plaintext
  aes.do_aes_encrypt(
      (byte *)plaintext,       // Input plaintext
      plaintext_len,           // Length of plaintext
      ciphertext,              // Output ciphertext
      aes_key,                 // AES key
      128,                     // Key size in bits
      aes_iv_enc                   // Initialization vector
  );

  // ---- Trigger LOW efter kryptering ----
  digitalWrite(triggerPin, LOW);
  Serial.println("Encryption done.");

  // Serial.print("Ciphertext (Hex): ");
  // for (size_t i = 0; i < plaintext_len; i++) {
  //     Serial.print(ciphertext[i], HEX);
  // }
  // Serial.println();

  // // Decrypt the ciphertext
  // aes.do_aes_decrypt(
  //     ciphertext,              // Input ciphertext
  //     plaintext_len,           // Length of ciphertext
  //     decrypted,               // Output plaintext
  //     aes_key,                 // AES key
  //     128,                     // Key size in bits
  //     aes_iv_dec                   // Initialization vector
  // );

  // Serial.print("Decrypted Text: ");
  // for (size_t i = 0; i < plaintext_len; i++) {
  //     Serial.print((char)decrypted[i]);
  // }
  // Serial.println();
}

void loop() {
  // Nothing to do here
}
