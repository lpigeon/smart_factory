#include <Servo.h>

#define IR_SENSOR_1 11
#define IR_SENSOR_2 12
#define IR_SENSOR_3 13
#define MOTOR 5

unsigned int state = 0;
unsigned int air_state = 0;

#define SERVO_1 9
#define SERVO_2 8
#define SERVO_3 7
Servo servo_1;
Servo servo_2;
Servo servo_3;

#define PUMP_PIN  6
#define SOLVALVE_PIN  10
Servo servo_pump;
Servo servo_solvalve;

unsigned long currTime = 0;
unsigned long prevTime = 0;

void setup() {
  Serial.begin(9600);
  pinMode(IR_SENSOR_1,INPUT);
  pinMode(IR_SENSOR_2,INPUT);
  pinMode(IR_SENSOR_3,INPUT);

  servo_1.attach(SERVO_1);
  servo_2.attach(SERVO_2);
  servo_3.attach(SERVO_3);

  servo_pump.attach(PUMP_PIN);
  servo_solvalve.attach(SOLVALVE_PIN);
  servo_pump.write(0);
  servo_solvalve.write(0);

  servo_1.write(79);
  servo_2.write(180);
  servo_3.write(103);
}

void loop() {
  int ir_sensor_1, ir_sensor_2, ir_sensor_3;
  ir_sensor_1 = digitalRead(IR_SENSOR_1);
  ir_sensor_2 = digitalRead(IR_SENSOR_2);
  ir_sensor_3 = digitalRead(IR_SENSOR_3);

  if(state == 0){
    Serial.println("0");
    if(ir_sensor_3 ==0){
      analogWrite(MOTOR,255);
      state = 1;
    }
  }
  else if(state == 1){
    Serial.println("1");
    if(ir_sensor_1 == 0){
      delay(300);
      analogWrite(MOTOR,0);
      state = 2;
    }
  }
  else if(state == 2){ //물건 들기
    Serial.println("2");
    servo_1.write(130);
    servo_2.write(180);
    servo_3.write(100);
    delay(500);

    
    servo_solvalve.write(0); //공기 풀기
    servo_pump.write(180); ////펌프 가동 빨아들이기
    delay(200);
    servo_pump.write(0); //펌프 멈춤
    air_state = 1;

    state = 3;
  }
  else if(state == 3){ //물건 들기
    Serial.println("3");
    servo_1.write(72);
    servo_2.write(180);
    servo_3.write(100);
    delay(1000);
    state = 4;
  }
  else if(state == 4){ //물건 들기
    Serial.println("4");
    servo_1.write(72);
    servo_2.write(90);
    servo_3.write(100);
    delay(1000);
    state = 5;
  }
  else if(state == 5){ //물건 들기
    Serial.println("5");
    servo_1.write(140);
    servo_2.write(90);
    servo_3.write(100);
    delay(1000);
    state = 6;
  }
  else if(state == 6){ //물건 들기
    Serial.println("6");
    servo_solvalve.write(180);
    servo_1.write(79);
    servo_2.write(180);
    servo_3.write(100);
    delay(1000);
    air_state = 0;
    state = 0;
  }


  currTime = millis();
  if(currTime - prevTime >= 1000)
  {
    prevTime = currTime;
    if(air_state == 1)
    {
      servo_solvalve.write(0); //공기 풀기
      servo_pump.write(180); ////펌프 가동 빨아들이기
      delay(200);
      servo_pump.write(0); //펌프 멈춤
    }
  }
}
