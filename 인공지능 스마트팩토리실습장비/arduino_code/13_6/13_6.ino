String strData1 = "hello arduino python";

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print("hello의 위치: ");
  Serial.println(strData1.indexOf("hello"));
  
  Serial.print("arduino의 위치: ");
  Serial.println(strData1.indexOf("arduino"));

  Serial.print("python의 위치: ");
  Serial.println(strData1.indexOf("python"));

  Serial.print("hi의 위치: ");
  Serial.println(strData1.indexOf("hi"));
  delay(2000);
}
