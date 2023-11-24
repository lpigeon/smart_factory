#include <Servo.h>

#define PUMP_PIN  6
#define SOLVALVE_PIN  10
Servo servo_pump;
Servo servo_solvalve;

bool catchState = 0;


void setup()   {
  Serial.begin(9600);

  servo_pump.attach(PUMP_PIN);
  servo_solvalve.attach(SOLVALVE_PIN);
  servo_pump.write(0);
  servo_solvalve.write(0);
}

void loop() {
  if (Serial.available() > 0) { 
    String inputData = Serial.readStringUntil('\n'); 
    inputData.trim(); 

    if (inputData.startsWith("CATCH=ON")) { 
      servo_solvalve.write(0); //공기 풀기
      servo_pump.write(180); //펌프 가동 빨아들이기
      catchState = 1;
      Serial.println("OK_CATCH=ON");
    }
    else if (inputData.startsWith("CATCH=OFF")) { 
      servo_solvalve.write(180); //물건놓기
      servo_pump.write(0); //펌프 멈춤
      catchState = 0;
      Serial.println("OK_CATCH=OFF");
    }
  }

  catchAction(catchState);
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
