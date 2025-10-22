#define buzzer 3
#define button1 8
#define button2 7
#define button3 6
#define button4 5
#define pass "4443"

int bools = 0b0000;
String curPass = "";

void victoryBuzz(int buzzerPin) {
  digitalWrite(buzzerPin, HIGH);
  delay(2);
  digitalWrite(buzzerPin, LOW);
}

void wrongBuzz(int buzzerPin) {
  digitalWrite(buzzerPin, HIGH);
  delay(2);
  digitalWrite(buzzerPin, LOW);
}

void buttonBuzz(int buzzerPin) {
  digitalWrite(buzzerPin, HIGH);
  delay(2);
  digitalWrite(buzzerPin, LOW);
}

void setup() {
  Serial.begin(115200);
  pinMode(button1,INPUT_PULLUP);
  pinMode(button2,INPUT_PULLUP);
  pinMode(button3,INPUT_PULLUP);
  pinMode(button4,INPUT_PULLUP);
  
  pinMode(buzzer, OUTPUT);

}

void loop() {
  int read1 = digitalRead(button1);
  int read2 = digitalRead(button2);
  int read3 = digitalRead(button3);
  int read4 = digitalRead(button4);
 
  /*
  Serial.print(read1);
  Serial.print(" ");
  Serial.print(read2);
  Serial.print(" ");
  Serial.print(read3);
  Serial.print(" ");
  Serial.println(read4);
  */

  if (!read1 && !bitRead(bools, 0)) {
    bitSet(bools,0);
    curPass += "1";
    //buttonBuzz(buzzer);
  } else if (read1) {
    bitClear(bools,0);
  } if (!read2 && !bitRead(bools, 1)) {
    bitSet(bools,1);
    curPass += "2";
    //buttonBuzz(buzzer);
  } else if (read2) {
    bitClear(bools,1);
  } if (!read3 && !bitRead(bools, 2)) {
    bitSet(bools,2);
    curPass += "3";
    //buttonBuzz(buzzer);
  } else if (read3) {
    bitClear(bools,2);
  } if (!read4 && !bitRead(bools, 3)) {
    bitSet(bools,3);
    curPass += "4";
    //buttonBuzz(buzzer);
  } else if (read4) {
    bitClear(bools,3);
  }

  if (curPass.length() >= 4) {
    buttonBuzz(buzzer);
    if (curPass.equals(pass)) {
      Serial.println("You in");
      buttonBuzz(buzzer);
    } else {
      Serial.println("WRONG! DUMBASS");
      buttonBuzz(buzzer);
    }
    curPass = "";
    Serial.println(curPass);
  }

  delay(2);

}