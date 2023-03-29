// pin Numbers (connect en- to PWM pins, others to any Digitals pins)
// Motor Top
int enTop = 9;
int pTop = 8;
int nTop = 7;

// Motor Bottom
int enBottom = 5;
int pBottom = 4;
int nBottom = 3;


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

}

void loop() {

  // Uncomment below to run specific function. Change function argument for slow, medium, fast.
  
  NoSpin(medium);
  
  // Topspin(medium);
  
  // Backspin(medium);

}
