// pin Numbers (connect en- to PWM pins, others to any Digitals pins)
// Motor Top
int enTop = ;
int pTop = ;
int nTop = ;

// Motor Bottom
int enBottom = ;
int pBottom = ;
int nBottom = ;

// Motor Left
int enLeft = ;
int pLeft = ;
int nLeft = ;

// Motor Right
int enRight = ;
int pRight = ;
int nRight = ;

// fast medium slow definitions
int fast = 240;
int medium = 180;
int slow = 120;


void setup() {
  pinMode(enTop, OUTPUT);
  pinMode(pTop, OUTPUT);
  pinMode(nTop, OUTPUT);
  pinMode(enBottom, OUTPUT);
  pinMode(pBottom, OUTPUT);
  pinMode(nBottom, OUTPUT);
  pinMode(enLeft, OUTPUT);
  pinMode(pLeft, OUTPUT);
  pinMode(nLeft, OUTPUT);
  pinMode(enRight, OUTPUT);
  pinMode(pRight, OUTPUT);
  pinMode(nRight, OUTPUT);

}

void NoSpin(int speed) {
  // Turn the motors ON
  // Top CW
  digitalWrite(pTop, LOW); 
  digitalWrite(nTop, HIGH);
  analogWrite(enTop, speed);
  
  // Bottom C
  digitalWrite(pBottom, HIGH);
  digitalWrite(nBottom, LOW);
  analogWrite(enBottom, speed);

  // Left C
  digitalWrite(pLeft, HIGH);
  digitalWrite(nLeft, LOW);
  analogWrite(enLeft, 255);

  // Right CW
  digitalWrite(pRight, LOW);
  digitalWrite(nRight, HIGH);
  analogWrite(enRight, 255);
}

void Topspin(int speed) {
  // Turn the motors ON
  // Top CW
  digitalWrite(pTop, LOW);
  digitalWrite(nTop, HIGH);
  analogWrite(enTop, speed);
  
  // Bottom CW
  digitalWrite(pBottom, LOW);
  digitalWrite(nBottom, HIGH);
  analogWrite(enBottom, speed);

  // Left C
  digitalWrite(pLeft, HIGH);
  digitalWrite(nLeft, LOW);
  analogWrite(enLeft, 255);

  // Right CW
  digitalWrite(pRight, LOW);
  digitalWrite(nRight, HIGH);
  analogWrite(enRight, 255);
}

void Backspin(int speed) {
  // Turn the motors ON
  // Top C
  digitalWrite(pTop, HIGH);
  digitalWrite(nTop, LOW);
  analogWrite(enTop, speed);
  
  // Bottom C
  digitalWrite(pBottom, HIGH);
  digitalWrite(nBottom, LOW);
  analogWrite(enBottom, speed);

  // Left CW
  digitalWrite(pLeft, HIGH);
  digitalWrite(nLeft, LOW);
  analogWrite(enLeft, 255);

  // Right CW
  digitalWrite(pRight, LOW);
  digitalWrite(nRight, HIGH);
  analogWrite(enRight, 255);
}

void loop() {

  // Uncomment below to run specific function. Change function argument for slow, medium, fast.
  
  NoSpin(medium);
  
  // Topspin(medium);
  
  // Backspin(medium);

}
