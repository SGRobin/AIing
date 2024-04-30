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

class Motor {
  private:

  Servo leg;
  int offset;
  bool is_reversed;

  public:
  Motor(int attached_pin, int offset, bool is_reversed){
    this->leg.attach(attached_pin);
    this->offset=offset;
    this->is_reversed=is_reversed;
  }

  void write_angel(int angle) {
    angle = (angle < 140) ? angle : 140;
    angle = (angle > 40) ? angle : 40; 

    angle += this->offset;
    if (this->is_reversed) {
      angle = 180 - angle;
    }

    this->leg.write(angle);
  }
};



// Dictionary<int, int*> offsets = Dictionary<int, int*>();
// static Motor motors[18];
static Motor motors[3] = {
  Motor(5, -25, false),
  Motor(6, -43, false),
  Motor(7, -45, false),

  // Motor(14,-10, false),
  // Motor(15,-43, false),
  // Motor(16,-50, false),

  // Motor(22, 38, false),
  // Motor(23, 50, false),
  // Motor(24, 40, false),

  // Motor(18, 41, true),
  // Motor(19, 44, true),
  // Motor(20, 42, true),

  // Motor(1, 6, false),
  // Motor(2, 25,false),
  // Motor(3, 9, false),

  // Motor(11, -30, true),
  // Motor(12, 14, true),
  // Motor(13, 13, true)
};

void setup() {

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

  // Wait until python sends commands:
  while (Serial.available() < 18);
  Serial.readBytes(input, 18);

}



void set_motor_angles(unsigned char *angles) {
  for(int i = 0; i < 3; i++) {
    Serial.println("the angle is:");
    Serial.println(angles[i]);

    motors[i].write_angel(angles[i]);
  }

}
