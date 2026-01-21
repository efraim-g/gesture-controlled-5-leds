// Gesture Controlled 5 LEDs using ESP8266 (No WiFi)
int leds[] = {D1, D2, D3, D4, D5};  // LEDs connected to these GPIO pins

void setup() {
  Serial.begin(9600);  // Serial communication with Python
  for (int i = 0; i < 5; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);
  }
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read command from Python

    if (command == '1') {
      turnOffAll();
      digitalWrite(leds[0], HIGH);
    }
    else if (command == '2') {
      turnOffAll();
      digitalWrite(leds[0], HIGH);
      digitalWrite(leds[1], HIGH);
    }
    else if (command == '3') {
      turnOffAll();
      digitalWrite(leds[0], HIGH);
      digitalWrite(leds[1], HIGH);
      digitalWrite(leds[2], HIGH);
    }
    else if (command == '4') {
      turnOffAll();
      digitalWrite(leds[0], HIGH);
      digitalWrite(leds[1], HIGH);
      digitalWrite(leds[2], HIGH);
      digitalWrite(leds[3], HIGH);
    }
    else if (command == '5') {
      turnOffAll();
      for (int i = 0; i < 5; i++) {
        digitalWrite(leds[i], HIGH);
      }
    }
    else if (command == '0') {
      turnOffAll();
    }
  }
}

void turnOffAll() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(leds[i], LOW);
  }
}
