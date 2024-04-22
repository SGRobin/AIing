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

Dictionary<int, int*> offsets = Dictionary<int, int*>();


// int potpin = 0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin

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

  leg_5_1.attach(1);
  leg_5_2.attach(2);
  leg_5_3.attach(3);

  leg_6_1.attach(11);
  leg_6_2.attach(12);
  leg_6_3.attach(13);

  // initialize dictionary:
  offsets.set(&leg_1_1, new int[2] {-35, 0});
  offsets.set(&leg_2_1, new int[2] {-43, 0});
  offsets.set(&leg_3_1, new int[2] {-35, 0});
  offsets.set(&leg_4_1, new int[2] {-20, 0});
  offsets.set(&leg_5_1, new int[2] {-43, 0});
  offsets.set(&leg_6_1, new int[2] {-35, 0});

  offsets.set(&leg_1_2, new int[2] {-2, 0});
  offsets.set(&leg_2_2, new int[2] {10, 0});
  offsets.set(&leg_3_2, new int[2] {0, 0});
  offsets.set(&leg_4_2, new int[2] {1, 1});
  offsets.set(&leg_5_2, new int[2] {4, 1});
  offsets.set(&leg_6_2, new int[2] {2, 1});

  offsets.set(&leg_1_3, new int[2] {-4, 0});
  offsets.set(&leg_2_3, new int[2] {15, 0});
  offsets.set(&leg_3_3, new int[2] {-1, 0});
  offsets.set(&leg_4_3, new int[2] {-40, 1});
  offsets.set(&leg_5_3, new int[2] {4, 1});
  offsets.set(&leg_6_3, new int[2] {3, 1});

  // communication with python:
  Serial.begin(115200);
  Serial.setTimeout(1);

}


void loop() {

  val = 90;
  angel_rapper(leg_1_1, val);
  angel_rapper(leg_2_1, val);
  angel_rapper(leg_3_1, val);
  angel_rapper(leg_4_1, val);
  angel_rapper(leg_5_1, val);
  angel_rapper(leg_6_1, val);

  val = 150;
  angel_rapper(leg_1_2, val);
  angel_rapper(leg_2_2, val);
  angel_rapper(leg_3_2, val);
  angel_rapper(leg_4_2, val);
  angel_rapper(leg_5_2, val);
  angel_rapper(leg_6_2, val);

  val = 100;
  angel_rapper(leg_1_3, val);
  angel_rapper(leg_2_3, val);
  angel_rapper(leg_3_3, val);
  angel_rapper(leg_4_3, val);
  angel_rapper(leg_5_3, val);
  angel_rapper(leg_6_3, val);

  // wait for orders:

  unsigned char output[18];
  get_motor_angels(output);
  Serial.write(output, 18);


  while (Serial.available() < 18);
  unsigned char input[18];
  Serial.readBytes(input, 18);

  // digitalWrite(LED_BUILTIN, LOW);
  // if(offsets.get(&leg_1_1) == 35) {
  //   digitalWrite(LED_BUILTIN, HIGH);
  // }

  delay(150000);                       // wait for a second

}

void angel_rapper(Servo& servo, int angle) {
  angle = (angle < 150) ? angle : 150;
  angle = (angle > 30) ? angle : 30; 

  angle += offsets.get(&servo)[0];
  if (offsets.get(&servo)[1] == 1) {
    angle = 180 - angle;
  }


  servo.write(angle);
}

void get_motor_angels(unsigned char *arr){
  arr[0] = (unsigned char)leg_1_1.read() - offsets.get(&leg_1_1)[0];
  arr[1] = (unsigned char)leg_2_1.read() - offsets.get(&leg_2_1)[0];
  arr[2] = (unsigned char)leg_3_1.read() - offsets.get(&leg_3_1)[0];
  arr[3] = (unsigned char)leg_4_1.read() - offsets.get(&leg_4_1)[0];
  arr[4] = (unsigned char)leg_5_1.read() - offsets.get(&leg_5_1)[0];
  arr[5] = (unsigned char)leg_6_1.read() - offsets.get(&leg_6_1)[0];

  arr[6] = (unsigned char)leg_1_2.read() - offsets.get(&leg_1_2)[0];
  arr[7] = (unsigned char)leg_2_2.read() - offsets.get(&leg_2_2)[0];
  arr[8] = (unsigned char)leg_3_2.read() - offsets.get(&leg_3_2)[0];
  arr[9] = 180 - (unsigned char)leg_4_2.read() - offsets.get(&leg_4_2)[0];
  arr[10] = 180 - (unsigned char)leg_5_2.read() - offsets.get(&leg_5_2)[0];
  arr[11] = 180 - (unsigned char)leg_6_2.read() - offsets.get(&leg_6_2)[0];

  arr[12] = (unsigned char)leg_1_3.read() - offsets.get(&leg_1_3)[0];
  arr[13] = (unsigned char)leg_2_3.read() - offsets.get(&leg_2_3)[0];
  arr[14] = (unsigned char)leg_3_3.read() - offsets.get(&leg_3_3)[0];
  arr[15] = 180 - (unsigned char)leg_4_3.read() - offsets.get(&leg_4_3)[0];
  arr[16] = 180 - (unsigned char)leg_5_3.read() - offsets.get(&leg_5_3)[0];
  arr[17] = 180 - (unsigned char)leg_6_3.read() - offsets.get(&leg_6_3)[0];
}
