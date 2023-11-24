#define LAMP_RED  2
#define LAMP_YELLOW  3
#define LAMP_GREEN  4

void setup() {
  Serial.begin(9600);

  pinMode(LAMP_RED,OUTPUT);
  pinMode(LAMP_YELLOW,OUTPUT);
  pinMode(LAMP_GREEN,OUTPUT);
  digitalWrite(LAMP_RED,0);
  digitalWrite(LAMP_YELLOW,0);
  digitalWrite(LAMP_GREEN,0);
}

void loop() {
  if (Serial.available() > 0) {                       // 시리얼 버퍼에 데이터가 있는지 확인
    String inputData = Serial.readStringUntil('\n');  // 개행 문자까지 읽어서 문자열로 저장
    inputData.trim();                                 // 문자열의 공백 제거

    if (inputData.startsWith("LAMP_RED=ON")) {        
      digitalWrite(LAMP_RED,1); 
      Serial.println("OK_LAMP_RED=ON");
    }
    else if (inputData.startsWith("LAMP_RED=OFF")) {        
      digitalWrite(LAMP_RED,0);
      Serial.println("OK_LAMP_RED=OFF");
    }
    else if (inputData.startsWith("LAMP_GREEN=ON")) {        
      digitalWrite(LAMP_GREEN,1);
      Serial.println("OK_LAMP_GREEN=ON");
    }
    else if (inputData.startsWith("LAMP_GREEN=OFF")) {        
      digitalWrite(LAMP_GREEN,0);
      Serial.println("OK_LAMP_GREEN=OFF");
    }
    else if (inputData.startsWith("LAMP_YELLOW=ON")) {        
      digitalWrite(LAMP_YELLOW,1);
      Serial.println("OK_LAMP_YELLOW=ON");
    }
    else if (inputData.startsWith("LAMP_YELLOW=OFF")) {        
      digitalWrite(LAMP_YELLOW,0);
      Serial.println("OK_LAMP_YELLOW=OFF");
    }
  }
}
