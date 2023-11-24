String strPi = "3.141592";

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print("strPi:");
  Serial.print(strPi);
  Serial.print("  size:");
  Serial.println(sizeof(strPi));
  
  float numPi = strPi.toFloat();
  Serial.print("numData:");
  Serial.print(numPi);
  Serial.print("  size:");
  Serial.println(sizeof(numPi));
  
  delay(2000);
}
