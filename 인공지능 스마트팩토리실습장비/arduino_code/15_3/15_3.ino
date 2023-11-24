
#include <Servo.h>

//서보모터
#define SERVO_1 9
#define SERVO_2 8
#define SERVO_3 7
Servo servo_1;
Servo servo_2;
Servo servo_3;

int servo1Angle = 80; // 저장할 각도 변수
int servo2Angle = 180; // 저장할 각도 변수
int servo3Angle = 100; // 저장할 각도 변수

//펌프
#define PUMP_PIN  6
#define SOLVALVE_PIN  10
Servo servo_pump;
Servo servo_solvalve;

bool catchState = 0;

//근접센서
#define IR_SENSOR_1 11
#define IR_SENSOR_2 12
#define IR_SENSOR_3 13

//컨베이어 모터
#define CB_MOTOR 5
int cbMotorSpeed = 0;  // 저장할 각도 변수

//타워램프
#define LAMP_RED  2
#define LAMP_YELLOW  3
#define LAMP_GREEN  4

//가변저항
#define VR_1  A0
#define VR_2  A1
#define VR_3  A2

void setup()   {
  Serial.begin(9600);


  //서보모터
  servo_1.attach(SERVO_1);
  servo_2.attach(SERVO_2);
  servo_3.attach(SERVO_3);

  servo_1.write(servo1Angle); //높이
  servo_2.write(servo2Angle); //회전
  servo_3.write(servo3Angle); //길이

  //펌프
  servo_pump.attach(PUMP_PIN);
  servo_solvalve.attach(SOLVALVE_PIN);
  servo_pump.write(0);
  servo_solvalve.write(0);

  //근접센서
  pinMode(IR_SENSOR_1,INPUT);
  pinMode(IR_SENSOR_2,INPUT);
  pinMode(IR_SENSOR_3,INPUT);

  //컨베이어 모터
  analogWrite(CB_MOTOR, cbMotorSpeed);

  //타워램프
  pinMode(LAMP_RED,OUTPUT);
  pinMode(LAMP_YELLOW,OUTPUT);
  pinMode(LAMP_GREEN,OUTPUT);
  digitalWrite(LAMP_RED,0);
  digitalWrite(LAMP_YELLOW,0);
  digitalWrite(LAMP_GREEN,0);
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
    else if (inputData.startsWith("CATCH=ON")) { 
      servo_solvalve.write(0); //공기 풀기
      servo_pump.write(180); ////펌프 가동 빨아들이기
      catchState = 1;
      Serial.println("OK_CATCH=ON");
    }
    else if (inputData.startsWith("CATCH=OFF")) { 
      servo_solvalve.write(180); //물건놓기
      servo_pump.write(0); //펌프 멈춤
      catchState = 0;
      Serial.println("OK_CATCH=OFF");
    }
    else if (inputData.startsWith("CV_MOTOR=")) {          
      String valueStr = inputData.substring(9);       
      valueStr.trim();                               
      cbMotorSpeed = valueStr.toInt();                 
      cbMotorSpeed = constrain(cbMotorSpeed, 0, 255);  
      analogWrite(CB_MOTOR, cbMotorSpeed);            
      Serial.print("Ok_CV_MOTOR=");
      Serial.println(cbMotorSpeed);            
    }
    else if (inputData.startsWith("LAMP_RED=ON")) {        
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
    else if (inputData.startsWith("VR_1=?")) {  
      Serial.print("OK_VR_1=");
      Serial.println(analogRead(VR_1));
    }
    else if (inputData.startsWith("VR_2=?")) {        
      Serial.print("OK_VR_2=");
      Serial.println(analogRead(VR_2));
    }
    else if (inputData.startsWith("VR_3=?")) {        
      Serial.print("OK_VR_3=");
      Serial.println(analogRead(VR_3));
    }
  }

  //펌프가 동작하 상태면 1초마다 에어를 빨아들이는 동작
  catchAction(catchState); 

  //근접센서
  getPsSensor1();
  getPsSensor2();
  getPsSensor3();
}


void catchAction(int state){
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;
  static unsigned long pumpStartTime = 0;
  static unsigned long pumpRunning = 0;

  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    prevTime = currTime;

    if (state == 1)
    {
      servo_solvalve.write(0); //공기 풀기
      servo_pump.write(180); //펌프 가동 빨아들이기
      pumpStartTime = currTime; // 펌프 작동 시작 시간 기록
      pumpRunning = true; // 펌프 작동 상태를 true로 변경
    }
  }

  if (pumpRunning && currTime - pumpStartTime >= 200)
  {
    servo_pump.write(0); // 펌프 작동 종료
    pumpRunning = false; // 펌프 작동 상태를 false로 변경
  }
}

void getPsSensor1(){
  static int currValue = 0;
  static int prevValue = 0;

  currValue = digitalRead(IR_SENSOR_1);
  if(currValue != prevValue){
    prevValue = currValue;
    if(currValue==1) Serial.println("PS_1=OFF");
    else Serial.println("PS_1=ON");
  }
}

void getPsSensor2(){
  static int currValue = 0;
  static int prevValue = 0;

  currValue = digitalRead(IR_SENSOR_2);
  if(currValue != prevValue){
    prevValue = currValue;
    if(currValue==1) Serial.println("PS_2=OFF");
    else Serial.println("PS_2=ON");
  }
}

void getPsSensor3(){
  static int currValue = 0;
  static int prevValue = 0;

  currValue = digitalRead(IR_SENSOR_3);
  if(currValue != prevValue){
    prevValue = currValue;
    if(currValue==1) Serial.println("PS_3=OFF");
    else Serial.println("PS_3=ON");
  }
}
