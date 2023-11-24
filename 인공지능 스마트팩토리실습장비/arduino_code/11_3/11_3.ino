#define VR_1  A0
#define VR_2  A1
#define VR_3  A2

void setup() {
  Serial.begin(9600);
}

void loop() {
  int vr_1,vr_2,vr_3;
  vr_1 = analogRead(VR_1);
  vr_2 = analogRead(VR_2);
  vr_3 = analogRead(VR_3);

  Serial.print(vr_1);
  Serial.print(",");
  Serial.print(vr_2);
  Serial.print(",");
  Serial.println(vr_3);
}