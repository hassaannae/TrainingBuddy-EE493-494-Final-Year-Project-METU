#include <SoftwareSerial.h>
#include "VoiceRecognitionV3.h"

/**        
  Connection
  Arduino    VoiceRecognitionModule
   2   ------->     TX
   3   ------->     RX
*/
VR myVR(50,3);    // 3:RX 50:TX, you can choose your favourite pins.

uint8_t records[7]; // save record
uint8_t buf[64];


// led pins
int  buddy = 22; // stored on position 0 / 15
int  set_speed = 23; // stored on position 1 / 16
int  slow = 24; // stored on position 2 / 17
int  moderate = 25; // stored on position 3 /18
int  fast = 26; // stored on position 4 /19
int  set_angle = 27; // stored on position 5 /20
int  left = 28; // stored on position 6 /21
int  mid = 29; // stored on position 7 /22
int  right = 30; // stored on position 8 /23
int  change_spin = 31; // stored on position 9 /24
int  topspin = 32; // stored on position 10 /25
int  backspin = 33; // stored on position 11 /26
int  test = 34; // stored on position 30 /27


// Flags
bool BUDDY = false; // wake word


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
  
  pinMode(buddy, OUTPUT);
  pinMode(set_speed, OUTPUT);
  pinMode(slow, OUTPUT);
  pinMode(moderate, OUTPUT);
  pinMode(fast, OUTPUT);
  pinMode(set_angle, OUTPUT);
  pinMode(left, OUTPUT);
  pinMode(mid, OUTPUT);
  pinMode(right, OUTPUT);
  pinMode(change_spin, OUTPUT);
  pinMode(topspin, OUTPUT);
  pinMode(backspin, OUTPUT);
  pinMode(test, OUTPUT);
    
  if(myVR.clear() == 0){
    Serial.println("Recognizer cleared.");
  }else{
    Serial.println("Not find VoiceRecognitionModule.");
    Serial.println("Please check connection and restart Arduino.");
    while(1);
  }
  
  myVR.load(uint8_t(0)); // Hey Buddy is stored on position 0
  myVR.load(uint8_t(15)); // Hey Buddy is stored on position 15
  myVR.load(uint8_t(30)); // test is stored on position 30
  myVR.load(uint8_t(27)); // test is stored on position 27
}

void loop()
{
  int ret;
  ret = myVR.recognize(buf, 50);
  if(ret>0){
    if (buf[1] == 0 || buf[1] == 15) {
      digitalWrite(buddy, HIGH);
      BUDDY = true;
      Serial.println("Hey Buddy");
      myVR.clear();
      myVR.load(uint8_t (1)); // set_speed
      myVR.load(uint8_t (16)); // set_speed
      myVR.load(uint8_t (5)); // set_angle
      myVR.load(uint8_t (20)); // set_angle
      myVR.load(uint8_t (9)); // change_spin
      myVR.load(uint8_t (24)); // change_spin
    }
    if (buf[1] == 30 || buf[1] == 27) {
      digitalWrite(test, HIGH);
      myVR.clear();
      myVR.load(uint8_t (0)); // buddy
      myVR.load(uint8_t (15)); // buddy
      myVR.load(uint8_t (30)); // test
      myVR.load(uint8_t (27)); // test
      delay(1000);
      digitalWrite(test, LOW);
    }

    if(BUDDY) {
      if(buf[1] == 1 || buf[1] == 16){
        digitalWrite(set_speed, HIGH);
        myVR.clear();
        myVR.load(uint8_t (2)); // slow
        myVR.load(uint8_t (17)); // slow
        myVR.load(uint8_t (3)); // medium
        myVR.load(uint8_t (18)); // medium
        myVR.load(uint8_t (4)); // fast
        myVR.load(uint8_t (19)); // fast
      }
      if(buf[1] == 2 || buf[1] == 17){
        digitalWrite(slow, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // buddy
        myVR.load(uint8_t (15)); // buddy
        delay(3000);
        digitalWrite(slow, LOW);
        digitalWrite(set_speed, LOW);
        digitalWrite(buddy, LOW);
      }
      if(buf[1] == 3 || buf[1] == 18){
        digitalWrite(moderate, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // buddy
        myVR.load(uint8_t (15)); // buddy
        delay(3000);
        digitalWrite(moderate, LOW);
        digitalWrite(set_speed, LOW);
        digitalWrite(buddy, LOW);
      }
      if(buf[1] == 4 || buf[1] == 19){
        digitalWrite(fast, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // buddy
        myVR.load(uint8_t (15)); // buddy
        delay(3000);
        digitalWrite(fast, LOW);
        digitalWrite(set_speed, LOW); 
        digitalWrite(buddy, LOW);      
      }      
      
      if(buf[1] == 5 || buf[1] == 20){
        digitalWrite(set_angle, HIGH);
        myVR.clear();
        myVR.load(uint8_t (6)); // left
        myVR.load(uint8_t (21)); // left
        myVR.load(uint8_t (7)); // mid
        myVR.load(uint8_t (22)); // mid
        myVR.load(uint8_t (8)); // right
        myVR.load(uint8_t (23)); // right
      }
      if(buf[1] == 6 || buf[1] == 21){
        digitalWrite(left, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // buddy
        myVR.load(uint8_t (15)); // buddy
        delay(3000);
        digitalWrite(left, LOW);
        digitalWrite(set_angle, LOW);  
        digitalWrite(buddy, LOW);      
      } 
      if(buf[1] == 7 || buf[1] == 22){
        digitalWrite(mid, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // buddy
        myVR.load(uint8_t (15)); // buddy
        delay(3000);
        digitalWrite(mid, LOW);
        digitalWrite(set_angle, LOW); 
        digitalWrite(buddy, LOW);      
      }
      if(buf[1] == 8 || buf[1] == 23){
        digitalWrite(right, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // buddy
        myVR.load(uint8_t (15)); // buddy
        delay(3000);
        digitalWrite(right, LOW);
        digitalWrite(set_angle, LOW);  
        digitalWrite(buddy, LOW);      
      }

      if(buf[1] == 9 || buf[1] == 24){
        digitalWrite(change_spin, HIGH);
        myVR.clear();
        myVR.load(uint8_t (10)); // Topspin
        myVR.load(uint8_t (25)); // Topspin
        myVR.load(uint8_t (11)); // Backspin
        myVR.load(uint8_t (26)); // Backspin
      }
      if(buf[1] == 10 || buf[1] == 25){
        digitalWrite(topspin, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // buddy
        myVR.load(uint8_t (15)); // buddy
        delay(3000);
        digitalWrite(topspin, LOW);
        digitalWrite(change_spin, LOW);
        digitalWrite(buddy, LOW);
      }
      if(buf[1] == 11 || buf[1] == 26){
        digitalWrite(backspin, HIGH);
        myVR.clear();
        myVR.load(uint8_t (0)); // buddy
        myVR.load(uint8_t (15)); // buddy
        delay(3000);
        digitalWrite(backspin, LOW);
        digitalWrite(change_spin, LOW);
        digitalWrite(buddy, LOW);
      }       
    }
    
    /** voice recognized */
    printVR(buf);
  }
}
