#define IR_SENSOR_1 11
#define IR_SENSOR_2 12
#define IR_SENSOR_3 13


void setup()   {
  Serial.begin(9600);

  pinMode(IR_SENSOR_1,INPUT);
  pinMode(IR_SENSOR_2,INPUT);
  pinMode(IR_SENSOR_3,INPUT);
}

void loop() {
  getPsSensor1();
  getPsSensor2();
  getPsSensor3();
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
