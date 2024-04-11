#include <Servo.h>
#include <Dictionary.h>

Servo leg_1_1; // 5
Servo leg_1_2; // 6
Servo leg_1_3; // 7

Servo leg_2_1; // 14
Servo leg_2_2; // 15
Servo leg_2_3; // 16

Servo leg_3_1; // 22
Servo leg_3_2; // 23
Servo leg_3_3; // 24

Servo leg_4_1; // 18
Servo leg_4_2; // 19
Servo leg_4_3; // 20

Servo leg_5_1; // 1
Servo leg_5_2; // 2
Servo leg_5_3; // 3

Servo leg_6_1; // 11
Servo leg_6_2; // 12
Servo leg_6_3; // 13

Dictionary<int, int> offsets = Dictionary<int, int>();

// void angel_rapper(&servo, angle) {
//   angle = angle
//   servo.write(angle)


// }

// int potpin = 0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin

void setup() {
  // attaching servos to GPIO pins:
  leg_1_1.attach(5);
  // leg_1_2.attach(6);
  // leg_1_3.attach(7);

  // leg_2_1.attach(14);
  // leg_2_2.attach(15);
  // leg_2_3.attach(16);

  // leg_3_1.attach(22);
  // leg_3_2.attach(23);
  // leg_3_3.attach(24);

  // leg_4_1.attach(18);
  // leg_4_2.attach(19);
  // leg_4_3.attach(20);

  // leg_5_1.attach(1);
  // leg_5_2.attach(2);
  // leg_5_3.attach(3);

  // leg_6_1.attach(11);
  // leg_6_2.attach(12);
  // leg_6_3.attach(13);

  // initialize dictionary:
  offsets.set(&leg_1_1, 35);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // val = 90;
  // leg_1_1.write(val - 35);
  // leg_2_1.write(val - 43);
  // leg_3_1.write(val - 35);
  // leg_4_1.write(val - 20);
  // leg_5_1.write(val - 43);
  // leg_6_1.write(val - 35);

  // val = 120;
  // leg_1_2.write(val);
  // leg_2_2.write(val);
  // leg_3_2.write(val);
  // leg_4_2.write(180 - val);
  // leg_5_2.write(180 - val);
  // leg_6_2.write(180 - val);

  // val = 80;
  // leg_1_3.write(val);
  // leg_2_3.write(val);
  // leg_3_3.write(val);
  // leg_4_3.write(180 - val);
  // leg_5_3.write(180 - val);
  // leg_6_3.write(180 - val);

  digitalWrite(LED_BUILTIN, LOW);
  if(offsets.get(&leg_1_1) == 35) {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  delay(15000);                       // wait for a second

}