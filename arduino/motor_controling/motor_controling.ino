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

Servo leg_5_1; // 9 - because pins 0 and 1 dont work
Servo leg_5_2; // 2
Servo leg_5_3; // 3

Servo leg_6_1; // 11
Servo leg_6_2; // 12
Servo leg_6_3; // 13

Dictionary<int, int*> offsets = Dictionary<int, int*>();

void setup() {
  // attaching servos to GPIO pins:
  leg_1_1.attach(5);
  leg_1_2.attach(6);
  leg_1_3.attach(7);

  leg_2_1.attach(14);
  leg_2_2.attach(15);
  leg_2_3.attach(16);

  leg_3_1.attach(22);
  leg_3_2.attach(23);
  leg_3_3.attach(24);

  leg_4_1.attach(18);
  leg_4_2.attach(19);
  leg_4_3.attach(20);

  leg_5_1.attach(9);
  leg_5_2.attach(2);
  leg_5_3.attach(3);

  leg_6_1.attach(11);
  leg_6_2.attach(12);
  leg_6_3.attach(13);

  // initialize dictionary:
  offsets.set(&leg_1_1, new int[2] {-25, 0});
  offsets.set(&leg_2_1, new int[2] {-43, 0});
  offsets.set(&leg_3_1, new int[2] {-45, 0});
  offsets.set(&leg_4_1, new int[2] {-10, 0});
  offsets.set(&leg_5_1, new int[2] {-43, 0});
  offsets.set(&leg_6_1, new int[2] {-50, 0});

  offsets.set(&leg_1_2, new int[2] {38, 0});
  offsets.set(&leg_2_2, new int[2] {50, 0});
  offsets.set(&leg_3_2, new int[2] {40, 0});
  offsets.set(&leg_4_2, new int[2] {41, 1});
  offsets.set(&leg_5_2, new int[2] {44, 1});
  offsets.set(&leg_6_2, new int[2] {10, 1});

  offsets.set(&leg_1_3, new int[2] {6, 0});
  offsets.set(&leg_2_3, new int[2] {25, 0});
  offsets.set(&leg_3_3, new int[2] {9, 0});
  offsets.set(&leg_4_3, new int[2] {-30, 1});
  offsets.set(&leg_5_3, new int[2] {14, 1});
  offsets.set(&leg_6_3, new int[2] {13, 1});

  // communication with python:
  Serial.begin(115200);
  Serial.setTimeout(1);

}


unsigned char val_1 = 90;
unsigned char val_2 = 90;
unsigned char val_3 = 90;
unsigned char input[18] = {val_1, val_1, val_1, val_1, val_1, val_1, val_2, val_2, val_2, val_2, val_2, val_2, val_3, val_3, val_3, val_3, val_3, val_3};

void loop() {

  set_motor_angles(input);

  while (Serial.available() < 18);
  Serial.readBytes(input, 18);

}

void angel_rapper(Servo& servo, int angle) {
  angle = (angle < 140) ? angle : 140;
  angle = (angle > 40) ? angle : 40; 

  angle += offsets.get(&servo)[0];
  if (offsets.get(&servo)[1] == 1) {
    angle = 180 - angle;
  }

  
  servo.write(angle);
}

void set_motor_angles(unsigned char *angles) {
  angel_rapper(leg_1_1, angles[0]);
  angel_rapper(leg_2_1, angles[1]);
  angel_rapper(leg_3_1, angles[2]);
  angel_rapper(leg_4_1, angles[3]);
  angel_rapper(leg_5_1, angles[4]);
  angel_rapper(leg_6_1, angles[5]);

  angel_rapper(leg_1_2, angles[6]);
  angel_rapper(leg_2_2, angles[7]);
  angel_rapper(leg_3_2, angles[8]);
  angel_rapper(leg_4_2, angles[9]);
  angel_rapper(leg_5_2, angles[10]);
  angel_rapper(leg_6_2, angles[11]);

  angel_rapper(leg_1_3, angles[12]);
  angel_rapper(leg_2_3, angles[13]);
  angel_rapper(leg_3_3, angles[14]);
  angel_rapper(leg_4_3, angles[15]);
  angel_rapper(leg_5_3, angles[16]);
  angel_rapper(leg_6_3, angles[17]);
}