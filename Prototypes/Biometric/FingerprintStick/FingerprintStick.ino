/* MODIFIED TO PERFORM FASTER ON OUR SPECIFIC HARDWARE
   YOUR MILEAGE MAY VARY.
   -> ragulbalaji Nov 2019
*/

#include <M5StickC.h>
#include "finger.h"
#include <ESP32Servo.h>

#define LID_CLOSE 160
#define LID_OPEN 50

uint8_t userNum; //User number
FingerPrint FP_M;
Servo lockservo;

void clearScreen() {
  M5.Lcd.fillRect(0, 0, 400, 300, BLACK);
  M5.Lcd.setCursor(0, 0);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setTextColor(WHITE);
  userNum = FP_M.fpm_getUserNum();
  //M5.Lcd.print("userNum:");
  //M5.Lcd.println(userNum);
}

void reeconnect() {
  Serial2.end();
  delay(100);
  Serial2.begin(19200, SERIAL_8N1, 33, 32);
}

void openLid(int pos){ // Do not use
  lockservo.attach(26);
  
  int val = 0;
  if(pos == 0) val = 150;
  else if(pos == 1) val = 70;
  
  lockservo.write(val);
  delay(3000);
  lockservo.detach();
}

void setup() {
  M5.begin();
  //Serial.begin(115200);
  Serial2.begin(19200, SERIAL_8N1, 33, 32);
  
  lockservo.attach(26);
  lockservo.write(LID_CLOSE);
  
  M5.Lcd.setRotation(3);
  clearScreen();
  M5.Lcd.setCursor(0, 0);
  M5.Lcd.setTextSize(3);
  M5.Lcd.setTextColor(RED);
  M5.Lcd.println("deLight BioLock!");

  M5.Lcd.setTextSize(1);
  M5.Lcd.setTextColor(WHITE);

  userNum = FP_M.fpm_getUserNum();
  //M5.Lcd.setCursor(0, 50);
  //M5.Lcd.print("userNum:");
  //M5.Lcd.println(userNum);
}

void loop() {
  uint8_t res1;

  if (M5.BtnA.wasPressed()) { // Big Button for Matching
    clearScreen();
    M5.Lcd.setTextColor(RED);
    M5.Lcd.println("deTouchID");
    M5.Lcd.setTextColor(WHITE);
    M5.Lcd.println("Place Finger");
    delay(1000); // Wait for user! Observation from trail run.
    M5.Lcd.println("Scanning...");
    res1 = FP_M.fpm_compareFinger();
    if (res1 == ACK_SUCCESS) {
      M5.Lcd.setTextColor(GREEN);
      M5.Lcd.println("Success!"); // Time to unlock

      lockservo.write(LID_OPEN);
      
      clearScreen();
      M5.Lcd.setTextColor(RED);
      M5.Lcd.println("Press Button to Close Lid.");

      do{
        M5.update();
        delay(10);
      }while(!M5.BtnA.wasPressed());
      
      lockservo.write(LID_CLOSE);

      M5.Lcd.println("\n<3 <3 <3");
    } else if (res1 == ACK_NOUSER) {
      M5.Lcd.println("Try Again :(");
    } else if (res1 == ACK_TIMEOUT) {
      M5.Lcd.println("Try Again :(");
      reeconnect();
    }
  } else if (M5.BtnB.wasPressed()) { // Side Button for Enrollment
    clearScreen();
    M5.Lcd.setTextColor(ORANGE);
    M5.Lcd.println("Enrol Finger!");
    M5.Lcd.setTextColor(WHITE);
    M5.Lcd.println("Place Finger");
    delay(1000); // Wait for user! Observation from trail run.
    M5.Lcd.println("Scanning...");

    userNum = FP_M.fpm_getUserNum();
    res1 = FP_M.fpm_addUser(userNum, 1);
    if (res1 == ACK_SUCCESS) {
      M5.Lcd.println("Success!");
      userNum++;
    } else if (res1 == ACK_FAIL) {
      M5.Lcd.println("Try Again :(");
      reeconnect();
    }
    else if (res1 == ACK_FULL) {
      M5.Lcd.println("Full");
    }
    else {
      M5.Lcd.println("Try Again :(");
      reeconnect();
    }

  }

  M5.update();
}
