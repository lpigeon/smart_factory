#define BUTTON_PIN  A3  

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN,INPUT_PULLUP);
}

void loop() {
  int btnValue = digitalRead(BUTTON_PIN);
  Serial.println(btnValue);
  delay(100);
}
