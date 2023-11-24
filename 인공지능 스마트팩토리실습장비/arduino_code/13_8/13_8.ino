String strData1 = "hello arduino python";

void setup() {
  Serial.begin(9600);
}

void loop() {
  if(strData1.indexOf("arduino") != -1)
  {
    Serial.println("arduino를 찾았습니다");
  }
  delay(2000);
}