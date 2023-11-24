#define MOTOR 5

void setup() {
  Serial.begin(9600);
}

void loop() {
  analogWrite(MOTOR,0);
  delay(2000);
  analogWrite(MOTOR,100);
  delay(2000);
  analogWrite(MOTOR,255);
  delay(2000);
}