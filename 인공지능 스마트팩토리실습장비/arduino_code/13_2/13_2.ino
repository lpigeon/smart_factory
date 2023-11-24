String strData1 = "hello";
String strData2 = "arduino";

void setup() {
  Serial.begin(9600);
}

void loop() {
  String strData3 = strData1 + " " + strData2;
  Serial.println(strData3);
  delay(2000);
}
