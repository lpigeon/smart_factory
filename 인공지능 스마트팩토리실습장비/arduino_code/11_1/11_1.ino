#define IR_SENSOR_1 13
#define IR_SENSOR_2 12
#define IR_SENSOR_3 11

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

  Serial.print(ir_sensor_1);
  Serial.print(",");
  Serial.print(ir_sensor_2);
  Serial.print(",");
  Serial.println(ir_sensor_3);
}
