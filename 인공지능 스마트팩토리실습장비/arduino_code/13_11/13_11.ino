String strData = "123";

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print("strData:");
  Serial.print(strData);
  Serial.print("  size:");
  Serial.println(sizeof(strData));
  
  int numData = strData.toInt();
  Serial.print("numData:");
  Serial.print(numData);
  Serial.print("  size:");
  Serial.println(sizeof(numData));
  
  delay(2000);
}
