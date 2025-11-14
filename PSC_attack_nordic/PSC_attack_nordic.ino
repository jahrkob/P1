/*
 * PSC Attack Demo for Nordic Semiconductor nRF52 Series
 * Compatible with nRF52832, nRF52840, and similar boards
 * 
 * This version is optimized for Nordic Semiconductor hardware
 * with support for BLE capabilities and low-power operation
 */

// Pin definitions for Nordic nRF52 boards
// Adjust these based on your specific Nordic board model
#define buzzer 3
#define button1 8
#define button2 7
#define button3 6
#define button4 5
#define pass "4443"

// State management using bit flags for efficient memory usage
int bools = 0b0000;
String curPass = "";

// Buzzer control functions
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
  // Nordic nRF52 series typically support higher baud rates
  // Using 115200 for compatibility with power analysis tools
  Serial.begin(115200);
  
  // Configure button pins with internal pull-up resistors
  // Nordic chips have strong pull-up/pull-down capabilities
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  pinMode(button3, INPUT_PULLUP);
  pinMode(button4, INPUT_PULLUP);
  
  pinMode(buzzer, OUTPUT);
  
  // Optional: Print Nordic chip information
  Serial.println("PSC Attack Demo - Nordic nRF52 Series");
  Serial.println("Waiting for button input...");
}

void loop() {
  // Read button states
  int read1 = digitalRead(button1);
  int read2 = digitalRead(button2);
  int read3 = digitalRead(button3);
  int read4 = digitalRead(button4);
 
  // Debug output (commented out for production use)
  /*
  Serial.print(read1);
  Serial.print(" ");
  Serial.print(read2);
  Serial.print(" ");
  Serial.print(read3);
  Serial.print(" ");
  Serial.println(read4);
  */

  // Button 1 handling with debouncing via bit flags
  if (!read1 && !bitRead(bools, 0)) {
    bitSet(bools, 0);
    curPass += "1";
    //buttonBuzz(buzzer);
  } else if (read1) {
    bitClear(bools, 0);
  }
  
  // Button 2 handling
  if (!read2 && !bitRead(bools, 1)) {
    bitSet(bools, 1);
    curPass += "2";
    //buttonBuzz(buzzer);
  } else if (read2) {
    bitClear(bools, 1);
  }
  
  // Button 3 handling
  if (!read3 && !bitRead(bools, 2)) {
    bitSet(bools, 2);
    curPass += "3";
    //buttonBuzz(buzzer);
  } else if (read3) {
    bitClear(bools, 2);
  }
  
  // Button 4 handling
  if (!read4 && !bitRead(bools, 3)) {
    bitSet(bools, 3);
    curPass += "4";
    //buttonBuzz(buzzer);
  } else if (read4) {
    bitClear(bools, 3);
  }

  // Password validation
  if (curPass.length() >= 4) {
    buttonBuzz(buzzer);
    if (curPass.equals(pass)) {
      Serial.println("You in");
      buttonBuzz(buzzer);
    } else {
      Serial.println("WRONG!");
      buttonBuzz(buzzer);
    }
    curPass = "";
    Serial.println(curPass);
  }

  // Nordic nRF52 has excellent power management
  // Short delay for responsive button detection
  delay(2);
}
