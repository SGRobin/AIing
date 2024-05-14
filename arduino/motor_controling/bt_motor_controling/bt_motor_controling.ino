#include <Servo.h>

typedef unsigned char byte_t;

class Motor {
    private:

    Servo servo;
    int pin;
    int offset;
    bool is_reversed;
    byte_t angle;

    public:

    Motor(int pin, int offset, bool is_reversed){
        this->pin = pin;
        this->offset = offset;
        this->is_reversed = is_reversed;
    }

    void init(){
      this->servo.attach(this->pin);
    }

    void set_angle(byte_t angle){
        if (abs(angle - this->angle) < 2) return;
        this->angle = angle;

        angle = (angle < 140) ? angle : 140;
        angle = (angle > 40) ? angle : 40; 

        angle += this->offset;
        if (this->is_reversed) angle = 180 - angle;

        this->servo.write(angle);
    }

};

Motor motors[18] = {
          Motor(7, -25, false), // leg_1_1
          Motor(14, -43, false), // leg_2_1
          Motor(22, -45, false), // leg_3_1
          Motor(28, -10, false), // leg_4_1 18
          Motor(3, -43, false), // leg_5_1
          Motor(11, -50, false), // leg_6_1 # used to be 11 but needed pin for BT
          Motor(8, 48, false), // leg_1_2
          Motor(15, 60, false), // leg_2_2
          Motor(23, 50, false), // leg_3_2
          Motor(29, 51, true), // leg_4_2 19
          Motor(4, 54, true), // leg_5_2
          Motor(12, 42, true), // leg_6_2
          Motor(9, 6, false), // leg_1_3
          Motor(16, 25, false), // leg_2_3
          Motor(24, 9, false), // leg_3_3
          Motor(30, -30, true), // leg_4_3 20
          Motor(5, 14, true), // leg_5_3
          Motor(13, 13, true) // leg_6_3
};

void setup(){
  Serial1.begin(9600);
  Serial1.setTimeout(1);
  Serial.begin(115200);
  Serial.setTimeout(1);
  
  // move the motors:
  for (int i = 0; i<18; i++){
    motors[i].init();
  }

}

unsigned char val_1 = 90;
unsigned char val_2 = 90;
unsigned char val_3 = 90;
unsigned char input[18] = {val_1, val_1, val_1, val_1, val_1, val_1, val_2, val_2, val_2, val_2, val_2, val_2, val_3, val_3, val_3, val_3, val_3, val_3};

void loop(){

  for (int i = 0; i<18; i++){
    motors[i].set_angle(input[i]);
  }

  while (Serial1.available() < 18);
  Serial1.readBytes(input, 18);

}
