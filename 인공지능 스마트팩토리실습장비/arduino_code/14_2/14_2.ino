#define CB_MOTOR 5
int cbMotorSpeed = 0;  // 저장할 각도 변수

void setup() {
  Serial.begin(9600);
  analogWrite(CB_MOTOR, cbMotorSpeed);
}

void loop() {
  if (Serial.available() > 0) {                      
    String inputData = Serial.readStringUntil('\n'); 
    inputData.trim();                               

    if (inputData.startsWith("CV_MOTOR=")) {        
      String valueStr = inputData.substring(9);    
      valueStr.trim();                              
      cbMotorSpeed = valueStr.toInt();                 
      cbMotorSpeed = constrain(cbMotorSpeed, 0, 255);  
      analogWrite(CB_MOTOR, cbMotorSpeed);             
      Serial.print("Ok_CV_MOTOR=");
      Serial.println(cbMotorSpeed);                   
    }
  }
}
