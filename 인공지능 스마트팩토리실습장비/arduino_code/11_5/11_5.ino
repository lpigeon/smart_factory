#define MOTOR 5
#define VR_1  A0

void setup() {
  Serial.begin(9600);
}

void loop() {
  int vr_1 = analogRead(VR_1);
  int motorSpeed = vr_1 / 4;
  Serial.println(motorSpeed);
  analogWrite(MOTOR,motorSpeed);
}