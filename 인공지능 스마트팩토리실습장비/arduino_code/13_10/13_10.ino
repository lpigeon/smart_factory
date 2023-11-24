String strData1 = "hello arduino python";

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print("6부터 끝까지:");
  Serial.println(strData1.substring(6));

  Serial.print("6부터 13전까지:");
  Serial.println(strData1.substring(6, 13));

  Serial.print("0부터 5전까지:");
  Serial.println(strData1.substring(0, 5));
  delay(2000);
}
//4_1_10.ino
