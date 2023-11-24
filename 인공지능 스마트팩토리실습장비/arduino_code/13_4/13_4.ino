String strData1 = "hello arduino";

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (strData1.equals("hi") == 1)
  {
    Serial.println("hi를 찾았습니다");
  }

  if (strData1.equals("hello") == 1)
  {
    Serial.println("hello를 찾았습니다");
  }

  if (strData1.equals("hello arduino") == 1)
  {
    Serial.println("hello arduino를 찾았습니다");
  }
  delay(2000);
}
