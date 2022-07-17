#include <Servo.h>

Servo test_servo;

void setup() {
  test_servo.attach(9);
  Serial.begin(115200);
  test_servo.write(20);
  while (!Serial){
    
    ;
  }
}



const char TERM = '|';

void loop() {
  if (Serial.available() > 0){
    String cmd = Serial.readStringUntil(TERM);
    if (cmd  == "0"){
      ;
    }
    else if (cmd == "1"){
      test_servo.write(90);
    }
    delay(20);
  }

}
