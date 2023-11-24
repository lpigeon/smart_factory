String strData1 = "hello,arduino,python";

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print(",(콤마)의 위치: ");
  int index1 = strData1.indexOf(",");
  Serial.println(index1);

  Serial.print("두번째 ,(콤마)의 위치: ");
  Serial.println(strData1.indexOf(",",index1 + 1));
  delay(2000);
}
