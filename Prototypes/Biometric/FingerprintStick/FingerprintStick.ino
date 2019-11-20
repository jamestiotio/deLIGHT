/* MODIFIED TO PERFORM FASTER ON OUR SPECIFIC HARDWARE
 * YOUR MILEAGE MAY VARY.
 * -> ragulbalaji Nov 2019
 */

#include <M5StickC.h>
#include "finger.h"

uint8_t userNum; //User number
FingerPrint FP_M;

void clearScreen(){
    M5.Lcd.fillRect(0,0,400,300,BLACK);
    M5.Lcd.setCursor(0, 0); 
    M5.Lcd.setTextSize(2);
    M5.Lcd.setTextColor(WHITE);
    userNum = FP_M.fpm_getUserNum();
    //M5.Lcd.print("userNum:");
    //M5.Lcd.println(userNum);
}

void reeconnect(){
  Serial2.end();
  delay(100);
  Serial2.begin(19200, SERIAL_8N1, 33, 32);
}

void setup(){
    M5.begin();
    //Serial.begin(115200);
    Serial2.begin(19200, SERIAL_8N1, 33, 32);
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

void loop(){
  uint8_t res1;
   
  if(M5.BtnA.wasPressed()){
      clearScreen();
      M5.Lcd.setTextColor(RED);
      M5.Lcd.println("deTouchID");
      M5.Lcd.setTextColor(WHITE);
      M5.Lcd.println("Place Finger");
      delay(1000); // Wait for user! Observation from trail run.
      M5.Lcd.println("Scanning...");
      res1 = FP_M.fpm_compareFinger();
      if(res1 == ACK_SUCCESS){
          M5.Lcd.setTextColor(GREEN);
          M5.Lcd.println("Success!");
      }else if(res1 == ACK_NOUSER){
          M5.Lcd.println("Try Again :(");
      }else if(res1 == ACK_TIMEOUT){
          M5.Lcd.println("Try Again :(");
          reeconnect();
      }
    }

    M5.update();
}


/*#include <M5StickC.h>
#include "finger.h"

uint8_t userNum;           //User number
FingerPrint FP_M;

void CleanScreen()
{
    M5.Lcd.setTextColor(RED);
    M5.Lcd.fillRect(0,20,400,300,BLACK);
    M5.Lcd.setCursor(0, 20); 
    M5.Lcd.setTextSize(1);
    userNum = FP_M.fpm_getUserNum();
    M5.Lcd.print("userNum:");
    M5.Lcd.println(userNum);
}

void setup() {
    M5.begin();
    //Serial.begin(19200);
    Serial2.begin(19200, SERIAL_8N1, 33, 32);
    M5.Lcd.setRotation(3);
    //M5.Lcd.clear(BLACK);
    //M5.Lcd.setTextColor(YELLOW);
    //M5.Lcd.setTextFont(2);
    //M5.Lcd.setTextSize(3);
    M5.Lcd.setCursor(0, 0); 
    M5.Lcd.println("Finger example");
    
    M5.Lcd.setTextColor(WHITE);
    M5.Lcd.setCursor(0, 50); 
    userNum = FP_M.fpm_getUserNum();
    M5.Lcd.print("userNum:");
    M5.Lcd.println(userNum);
    
}

void reeconnect(){
  Serial2.end();
  delay(300);
  Serial2.begin(19200, SERIAL_8N1, 33, 32);
}

//ButtonA: Add user
//ButtonB: Matching
void loop(){
  
    uint8_t res1;
    if(M5.BtnA.wasPressed()){
        CleanScreen();
        M5.Lcd.println("Fingerprint Typing");
        
        res1 = FP_M.fpm_addUser(userNum,1);
        if(res1 == ACK_SUCCESS){
            M5.Lcd.println("Success");
        }
        else if(res1 == ACK_FAIL){
            M5.Lcd.println("Fail");
            reeconnect();
        }
        else if(res1 == ACK_FULL){
            M5.Lcd.println("Full");
        }
        else{
            M5.Lcd.println("Timeout");
            reeconnect();
        }
        userNum++;
    }

    if(M5.BtnB.wasPressed()){
      CleanScreen();
      M5.Lcd.println("Matching");
      
      res1 = FP_M.fpm_compareFinger();
      if(res1 == ACK_SUCCESS){
          M5.Lcd.println("Success");
      }
      if(res1 == ACK_NOUSER){
          M5.Lcd.println("No Such User");
      }
      if(res1 == ACK_TIMEOUT){
          M5.Lcd.println("Timeout");
          reeconnect();
      }
    }

    M5.update();
    
}*/
