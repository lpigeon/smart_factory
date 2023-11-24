String strData1 = "hello arduino";
String strData2 = "hello";
String strData3 = "arduino";

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print(strData1 + " 길이는: ");
  Serial.println(strData1.length());
  
  Serial.print(strData2 + " 길이는: ");
  Serial.println(strData2.length());
  
  Serial.print(strData3 + " 길이는: ");
  Serial.println(strData3.length());
  delay(2000);
}
