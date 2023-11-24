#include <Servo.h>

#define SERVO_1 9
#define SERVO_2 8
#define SERVO_3 7
Servo servo_1;
Servo servo_2;
Servo servo_3;

int servo1Angle = 80; // 저장할 각도 변수
int servo2Angle = 180; // 저장할 각도 변수
int servo3Angle = 100; // 저장할 각도 변수

void setup()   {
  Serial.begin(9600);

  servo_1.attach(SERVO_1);
  servo_2.attach(SERVO_2);
  servo_3.attach(SERVO_3);

  servo_1.write(servo1Angle); //높이
  servo_2.write(servo2Angle); //회전
  servo_3.write(servo3Angle); //길이
}

void loop() {
  if (Serial.available() > 0) { 
    String inputData = Serial.readStringUntil('\n');
    inputData.trim();

    if (inputData.startsWith("SERVO_1=")) { 
      String valueStr = inputData.substring(8); 
      valueStr.trim(); 
      servo1Angle = valueStr.toInt();
      servo1Angle = constrain(servo1Angle, 60, 130); 
      servo_1.write(servo1Angle); 
      Serial.print("OK_SERVO_1=");
      Serial.println(servo1Angle);
    }
    else if (inputData.startsWith("SERVO_2=")) { 
      String valueStr = inputData.substring(8);
      valueStr.trim(); 
      servo2Angle = valueStr.toInt();
      servo2Angle = constrain(servo2Angle, 0, 180); 
      servo_2.write(servo2Angle); 
      Serial.print("OK_SERVO_2=");
      Serial.println(servo2Angle);
    }
    else if (inputData.startsWith("SERVO_3=")) { 
      String valueStr = inputData.substring(8);
      valueStr.trim(); 
      servo3Angle = valueStr.toInt(); 
      servo3Angle = constrain(servo3Angle, 30, 120);
      servo_3.write(servo3Angle); 
      Serial.print("OK_SERVO_3=");
      Serial.println(servo3Angle);
    }
  }
}