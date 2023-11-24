#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define i2c_Address 0x3c

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64 
#define OLED_RESET -1  
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define VR_1  A0
#define VR_2  A1
#define VR_3  A2

void setup()   {
  Serial.begin(9600);

  delay(250);
  display.begin(i2c_Address, true);
}

void loop() {
  int vr_1,vr_2,vr_3;
  vr_1 = analogRead(VR_1);
  vr_2 = analogRead(VR_2);
  vr_3 = analogRead(VR_3);
  
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(0, 0);
  display.print("VR1: "); display.println(vr_1);
  display.print("VR2: "); display.println(vr_2);
  display.print("VR3: "); display.println(vr_3);
  display.display();
}
