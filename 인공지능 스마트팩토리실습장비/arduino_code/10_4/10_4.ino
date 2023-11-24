#define BUTTON_PIN  A3  

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN,INPUT_PULLUP);
}

void loop() {
  if(button_on() == 1){
    Serial.println("button click");
  }
}

int button_on(){
  static int prevBtn = 1;
  static int currBtn = 1;
  currBtn = digitalRead(BUTTON_PIN);
  if(currBtn != prevBtn){
    prevBtn = currBtn;
    delay(100);
    if(currBtn == 0)  return 1;
  }

  return 0;
}
