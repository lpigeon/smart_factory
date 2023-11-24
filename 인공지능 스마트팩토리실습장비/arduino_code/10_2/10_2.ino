#define LAMP_RED  2
#define LAMP_YELLOW  3
#define LAMP_GREEN  4

void setup() {
  pinMode(LAMP_RED,OUTPUT);
  pinMode(LAMP_YELLOW,OUTPUT);
  pinMode(LAMP_GREEN,OUTPUT);
}

void loop() {
  digitalWrite(LAMP_RED,HIGH);
  digitalWrite(LAMP_YELLOW,LOW);
  digitalWrite(LAMP_GREEN,LOW);
  delay(1000);
  digitalWrite(LAMP_RED,LOW);
  digitalWrite(LAMP_YELLOW,HIGH);
  digitalWrite(LAMP_GREEN,LOW);
  delay(1000);
  digitalWrite(LAMP_RED,LOW);
  digitalWrite(LAMP_YELLOW,LOW);
  digitalWrite(LAMP_GREEN,HIGH);
  delay(1000);
}