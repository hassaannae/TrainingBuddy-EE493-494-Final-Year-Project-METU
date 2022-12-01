#include <SoftwareSerial.h>
#include "VoiceRecognitionV3.h"

/**        
  Connection
  Arduino    VoiceRecognitionModule
   2   ------->     TX
   3   ------->     RX
*/
VR myVR(2,3);    // 2:RX 3:TX, you can choose your favourite pins.

uint8_t records[7]; // save record
uint8_t buf[64];


// led pins
int  hey_buddy = 22; // stored on position 0
int  power_on = 23; // stored on position 1
int  power_off = 24; // stored on position 2
int  set_speed = 25; // stored on position 3
int  set_frequency= 26; // stored on position 4
int  slow = 27; // stored on position 5
int  moderate = 28; // stored on position 6
int  fast = 29; // stored on position 7
int  set_angle = 30; // stored on position 8
int  left = 31; // stored on position 9
int  mid = 32; // stored on position 10
int  right = 33; // stored on position 11
int  change_spin = 35; // stored on position 12
int  no_spin = 36; // stored on position 13
int  topspin = 37; // stored on position 14
int  backspin = 38; // stored on position 15
int  heavy = 39; // stored on position 16
int  light = 40; // stored on position 17
//int  = 41;
//int  = 42;
//int  = 43;
//int  = 44;
//int  = 45;
//int  = 46;
//int  = 47;
//int  = 48;
//int  = 49;


// Flags
bool HEY_BUDDY = false; // wake word


#define onRecord    (0)
#define offRecord   (1) 

/**
  @brief   Print signature, if the character is invisible, 
           print hexible value instead.
  @param   buf     --> command length
           len     --> number of parameters
*/
void printSignature(uint8_t *buf, int len)
{
  int i;
  for(i=0; i<len; i++){
    if(buf[i]>0x19 && buf[i]<0x7F){
      Serial.write(buf[i]);
    }
    else{
      Serial.print("[");
      Serial.print(buf[i], HEX);
      Serial.print("]");
    }
  }
}

/**
  @brief   Print signature, if the character is invisible, 
           print hexible value instead.
  @param   buf  -->  VR module return value when voice is recognized.
             buf[0]  -->  Group mode(FF: None Group, 0x8n: User, 0x0n:System
             buf[1]  -->  number of record which is recognized. 
             buf[2]  -->  Recognizer index(position) value of the recognized record.
             buf[3]  -->  Signature length
             buf[4]~buf[n] --> Signature
*/
void printVR(uint8_t *buf)
{
  Serial.println("VR Index\tGroup\tRecordNum\tSignature");

  Serial.print(buf[2], DEC);
  Serial.print("\t\t");

  if(buf[0] == 0xFF){
    Serial.print("NONE");
  }
  else if(buf[0]&0x80){
    Serial.print("UG ");
    Serial.print(buf[0]&(~0x80), DEC);
  }
  else{
    Serial.print("SG ");
    Serial.print(buf[0], DEC);
  }
  Serial.print("\t");

  Serial.print(buf[1], DEC);
  Serial.print("\t\t");
  if(buf[3]>0){
    printSignature(buf+4, buf[3]);
  }
  else{
    Serial.print("NONE");
  }
  Serial.println("\r\n");
}

void setup()
{
  /** initialize */
  myVR.begin(9600);
  
  Serial.begin(115200);
  Serial.println("Voice Control Unit for Training Buddy");
  
  pinMode(hey_buddy, OUTPUT);
  pinMode(power_on, OUTPUT);
  pinMode(power_off, OUTPUT);
  pinMode(set_speed, OUTPUT);
  pinMode(set_frequency, OUTPUT);
  pinMode(slow, OUTPUT);
  pinMode(moderate, OUTPUT);
  pinMode(fast, OUTPUT);
  pinMode(set_angle, OUTPUT);
  pinMode(left, OUTPUT);
  pinMode(mid, OUTPUT);
  pinMode(right, OUTPUT);
  pinMode(change_spin, OUTPUT);
  pinMode(no_spin, OUTPUT);
  pinMode(topspin, OUTPUT);
  pinMode(backspin, OUTPUT);
  pinMode(heavy, OUTPUT);
  pinMode(light, OUTPUT);
    
  if(myVR.clear() == 0){
    Serial.println("Recognizer cleared.");
  }else{
    Serial.println("Not find VoiceRecognitionModule.");
    Serial.println("Please check connection and restart Arduino.");
    while(1);
  }
  
  myVR.load(uint8_t(0)); // Hey Buddy is stored on position 0
}

void loop()
{
  int ret;
  ret = myVR.recognize(buf, 50);
  if(ret>0){
    if (buf[1] == 0) {
      digitalWrite(hey_buddy, HIGH);
      HEY_BUDDY = true;
      Serial.println("Hey Buddy");
      myVR.clear();
      myVR.load(uint8_t (3)); // set_speed
      myVR.load(uint8_t (4)); // set_frequency
      myVR.load(uint8_t (8)); // set_angle
      myVR.load(uint8_t (12)); // change_spin
    }

    if(HEY_BUDDY) {
      if(buf[1] == 3){
        digitalWrite(set_speed, HIGH);
        myVR.clear();
        myVR.load(uint8_t (5)); // slow
        myVR.load(uint8_t (6)); // medium
        myVR.load(uint8_t (7)); // fast
      }
      if(buf[1] == 4){
        digitalWrite(set_frequency, HIGH);
        myVR.clear();
        myVR.load(uint8_t (5)); // slow
        myVR.load(uint8_t (6)); // medium
        myVR.load(uint8_t (7)); // fast
      }
      if(buf[1] == 5){
        digitalWrite(slow, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // hey_buddy
        delay(3000);
        digitalWrite(slow, LOW);
        digitalWrite(set_speed, LOW);
        digitalWrite(set_frequency, LOW);
        digitalWrite(hey_buddy, LOW);
      }
      if(buf[1] == 6){
        digitalWrite(moderate, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // hey_buddy
        delay(3000);
        digitalWrite(moderate, LOW);
        digitalWrite(set_speed, LOW);
        digitalWrite(set_frequency, LOW);
        digitalWrite(hey_buddy, LOW);
      }
      if(buf[1] == 7){
        digitalWrite(fast, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // hey_buddy
        delay(3000);
        digitalWrite(fast, LOW);
        digitalWrite(set_speed, LOW);
        digitalWrite(set_frequency, LOW);  
        digitalWrite(hey_buddy, LOW);      
      }      
      
      if(buf[1] == 8){
        digitalWrite(set_angle, HIGH);
        myVR.clear();
        myVR.load(uint8_t (9)); // slow
        myVR.load(uint8_t (10)); // medium
        myVR.load(uint8_t (11)); // fast
      }
      if(buf[1] == 9){
        digitalWrite(left, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // hey_buddy
        delay(3000);
        digitalWrite(left, LOW);
        digitalWrite(set_angle, LOW);  
        digitalWrite(hey_buddy, LOW);      
      } 
      if(buf[1] == 10){
        digitalWrite(mid, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // hey_buddy
        delay(3000);
        digitalWrite(mid, LOW);
        digitalWrite(set_angle, LOW); 
        digitalWrite(hey_buddy, LOW);      
      }
      if(buf[1] == 11){
        digitalWrite(right, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // hey_buddy
        delay(3000);
        digitalWrite(right, LOW);
        digitalWrite(set_angle, LOW);  
        digitalWrite(hey_buddy, LOW);      
      }

      if(buf[1] == 12){
        digitalWrite(change_spin, HIGH);
        myVR.clear();
        myVR.load(uint8_t (13)); // no spin
        myVR.load(uint8_t (14)); // Topspin
        myVR.load(uint8_t (15)); // Backspin
      }
      if(buf[1] == 13){
        digitalWrite(no_spin, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // hey_buddy
        delay(3000);
        digitalWrite(no_spin, LOW);
        digitalWrite(change_spin, LOW);  
        digitalWrite(hey_buddy, LOW);
      }
      if(buf[1] == 14){
        digitalWrite(topspin, HIGH);
        myVR.clear();
        myVR.load(uint8_t (16)); // heavy
        myVR.load(uint8_t (17)); // light
      }
      if(buf[1] == 15){
        digitalWrite(backspin, HIGH);
        myVR.clear();
        myVR.load(uint8_t (16)); // heavy
        myVR.load(uint8_t (17)); // light
      }
      if(buf[1] == 16){
        digitalWrite(heavy, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // hey_buddy
        delay(3000);
        digitalWrite(heavy, LOW);
        digitalWrite(topspin, LOW);
        digitalWrite(backspin, LOW);
        digitalWrite(change_spin, LOW);
        digitalWrite(hey_buddy, LOW);
      }
      if(buf[1] == 17){
        digitalWrite(light, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // hey_buddy
        delay(3000);
        digitalWrite(light, LOW);
        digitalWrite(topspin, LOW);
        digitalWrite(backspin, LOW);
        digitalWrite(change_spin, LOW);
        digitalWrite(hey_buddy, LOW);
      }        
    }
    
    /** voice recognized */
    printVR(buf);
  }
}
