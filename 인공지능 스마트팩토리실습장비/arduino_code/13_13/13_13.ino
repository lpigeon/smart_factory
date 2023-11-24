void setup() {
  Serial.begin(9600);
}

void loop() {
  String strData = "   hello arduino python    ";
  
  Serial.print("strData: ");
  Serial.println(strData);
  Serial.print("공백제거: ");
  strData.trim();
  Serial.println(strData);
  delay(2000);
}
