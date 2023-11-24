String strData1 = "hello arduino python";

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print("hello의 위치(뒤에서부터): ");
  Serial.println(strData1.lastIndexOf("hello"));
  
  Serial.print("arduino의 위치(뒤에서부터): ");
  Serial.println(strData1.lastIndexOf("arduino"));

  Serial.print("python의 위치(뒤에서부터): ");
  Serial.println(strData1.lastIndexOf("python"));

  Serial.print("hi의 위치(뒤에서부터): ");
  Serial.println(strData1.lastIndexOf("hi"));
  delay(2000);
}
