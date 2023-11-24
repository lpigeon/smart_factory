#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <Servo.h>

#define i2c_Address 0x3c

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64 
#define OLED_RESET -1  
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define VR_1  A0
#define VR_2  A1
#define VR_3  A2

int servo1Angle = 80; 
int servo2Angle = 180;
int servo3Angle = 100;

#define SERVO_1 9
#define SERVO_2 8
#define SERVO_3 7
Servo servo_1;
Servo servo_2;
Servo servo_3;

void setup()   {
  Serial.begin(9600);

  delay(250);
  display.begin(i2c_Address, true);

  servo_1.attach(SERVO_1);
  servo_2.attach(SERVO_2);
  servo_3.attach(SERVO_3);
  servo_1.write(servo1Angle);
  servo_2.write(servo2Angle);
  servo_3.write(servo3Angle);
}

void loop() {
  int vr_1,vr_2,vr_3;
  vr_1 = analogRead(VR_1);
  vr_2 = analogRead(VR_2);
  vr_3 = analogRead(VR_3);

  //가변저항 0~1023 값을 서보모터각도인 0~180로 변환
  vr_1 = map(vr_1, 0, 1023, 180, 0);
  vr_2 = map(vr_2, 0, 1023, 180, 0);
  vr_3 = map(vr_3, 0, 1023, 180, 0);

  //각 서보모터의 동작 범위를 제한
  servo1Angle = constrain(vr_1, 60, 130); 
  servo2Angle = constrain(vr_2, 0, 180);
  servo3Angle = constrain(vr_3, 30, 120);

  //OLED 디스플레
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(0, 0);
  display.print("SV1: "); display.println(servo1Angle);
  display.print("SV2: "); display.println(servo2Angle);
  display.print("SV3: "); display.println(servo3Angle);
  display.display();

  //서보모터 출력
  servo_1.write(servo1Angle);
  servo_2.write(servo2Angle);
  servo_3.write(servo3Angle);
}
