#include "SPI.h"
#include "MFRC522.h"
#include <Dictionary.h>

#define button1 4
#define button2 5
#define button3 6
#define button4 7

int bools = 0b0000;
String curPass = "";

#define _DICT_KEYLEN 64
#define _DICT_VALLEN 254
#define _DICT_CRC 64
#define SS_PIN 10
#define RST_PIN 9

Dictionary &known_cards = *(new Dictionary(6));

int BuzzerPin = 3;   // Status LED

MFRC522 rfid(SS_PIN, RST_PIN);

MFRC522::MIFARE_Key key;

String getInputPass() {
  Serial.println("Type password: ");
  curPass = "";
  while (true) {
    delay(10);
    int read1 = digitalRead(button1);
    int read2 = digitalRead(button2);
    int read3 = digitalRead(button3);
    int read4 = digitalRead(button4);

    if (!read1 && !bitRead(bools, 0)) {
      bitSet(bools,0);
      curPass += "1";
    } else if (read1) {
      bitClear(bools,0);
    } if (!read2 && !bitRead(bools, 1)) {
      bitSet(bools,1);
      curPass += "2";
    } else if (read2) {
      bitClear(bools,1);
    } if (!read3 && !bitRead(bools, 2)) {
      bitSet(bools,2);
      curPass += "3";
    } else if (read3) {
      bitClear(bools,2);
    } if (!read4 && !bitRead(bools, 3)) {
      bitSet(bools,3);
      curPass += "4";
    } else if (read4) {
      bitClear(bools,3);
    }

    if (curPass.length() >= 4) {
      return curPass;
      Serial.println(curPass);
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();
  pinMode(BuzzerPin, OUTPUT);
  Serial.println("I am waiting for card...");
  Serial.begin(115200);
  pinMode(button1,INPUT_PULLUP);
  pinMode(button2,INPUT_PULLUP);
  pinMode(button3,INPUT_PULLUP);
  pinMode(button4,INPUT_PULLUP);
}

void loop() {

  // put your main code here, to run repeatedly:
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial())
    return;

  // Serial.print(F("PICC type: "));
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  // Serial.println(rfid.PICC_GetTypeName(piccType));

  // Check is the PICC of Classic MIFARE type
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
      piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
      piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return;
  }
  String strID = "";
  for (byte i = 0; i < 4; i++) {
    strID +=
      (rfid.uid.uidByte[i] < 0x10 ? "0" : "") +
      String(rfid.uid.uidByte[i], HEX) +
      (i != 3 ? ":" : "");
  }

  strID.toUpperCase();
  Serial.print("Tap card key: ");
  Serial.println(strID);
  delay(500);

  if (!known_cards(strID)) {
    String pass = getInputPass();
    known_cards(strID, pass);
    Serial.print("Password set to: ");
    Serial.println(pass);
    return;
  }
  String pass = getInputPass();
  digitalWrite(BuzzerPin, HIGH);
  delay (5);
  digitalWrite(BuzzerPin, LOW);
  if (known_cards[strID] == pass) {  //put your own tap card key;
    Serial.println("********************");
    Serial.println("**Adgang Tilladt**");
    Serial.println("********************");
    digitalWrite(BuzzerPin, HIGH);
    delay (5);
    digitalWrite(BuzzerPin, LOW);
  } else {
    Serial.println("****************");
    Serial.println("**Adgang Nægtet**");
    Serial.println("****************");
    digitalWrite(BuzzerPin, HIGH);
    delay (5);
    digitalWrite(BuzzerPin, LOW);
  }
}