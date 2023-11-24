#define IR_SENSOR_1 11
#define IR_SENSOR_2 12
#define IR_SENSOR_3 13
#define MOTOR 5

unsigned int state = 0;

void setup() {
  Serial.begin(9600);
  pinMode(IR_SENSOR_1,INPUT);
  pinMode(IR_SENSOR_2,INPUT);
  pinMode(IR_SENSOR_3,INPUT);
}

void loop() {
  int ir_sensor_1, ir_sensor_2, ir_sensor_3;
  ir_sensor_1 = digitalRead(IR_SENSOR_1);
  ir_sensor_2 = digitalRead(IR_SENSOR_2);
  ir_sensor_3 = digitalRead(IR_SENSOR_3);

  if(state == 0){
    if(ir_sensor_3 ==0){
      analogWrite(MOTOR,255);
      state = 1;
    }
  }
  else if(state == 1){
    if(ir_sensor_1 == 0){
      analogWrite(MOTOR,0);
      state = 0;
    }
  }

  Serial.print(ir_sensor_1);
  Serial.print(",");
  Serial.print(ir_sensor_2);
  Serial.print(",");
  Serial.println(ir_sensor_3);
}