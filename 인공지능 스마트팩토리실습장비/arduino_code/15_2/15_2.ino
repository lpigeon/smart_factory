#define VR_1  A0
#define VR_2  A1
#define VR_3  A2

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {   
    String inputData = Serial.readStringUntil('\n'); 
    inputData.trim();                           

    if (inputData.startsWith("VR_1=?")) {  
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
}