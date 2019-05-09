#include <BluetoothSerial.h>
#include <Wire.h>
#include "BluetoothSerial.h"
#include <stdio.h>
#include <math.h>
#include <dummy.h>
#include <VL53L1X.h> //LIDAR sensor library

BluetoothSerial SerialBT;

//TwoWire I2C_ONE = TwoWire(0); //INIT LIDAR1 I2C BITBANG PIN
//TwoWire I2C_TWO = TwoWire(1); //INIT LIDAR2 I2C BITBANG PIN

VL53L1X LIDAR;

int count = 0;
#define PWM1pin 14 //LEFT DRIVE MOTOR
#define DIR1pin 32
const int PWM1channel = 0;

#define PWM2pin 15 // RIGHT DRIVE MOTOR
#define DIR2pin 12
const int PWM2channel = 0;

#define PWM3pin 36 // TRAWLER MOTOR
#define DIR3pin 39
const int PWM3channel = 0;


//const int IR_1pin = A0; // IR SENSORS
//const int IR_2pin = A1;

#define LASER_1 27
#define LASER_2 33



void setup() {
  Serial.begin(115200);
  SerialBT.begin("A R N I E"); //Bluetooth device name
  //Serial.println("The device started, now you can pair it with bluetooth!");
  //pinMode(13,OUTPUT);
  //digitalWrite(13,LOW);

  ledcSetup(PWM1channel,5000,8); // pwm channel, frequency, resolution in bits
  ledcAttachPin(PWM1pin,PWM1channel); // pin, pwm channel

  ledcSetup(PWM2channel,5000,8);
  ledcAttachPin(PWM2pin,PWM2channel);

  ledcSetup(PWM3channel,5000,8);
  ledcAttachPin(PWM3pin,PWM3channel);

  pinMode(DIR1pin, OUTPUT); // set direction pins to output
  pinMode(DIR2pin, OUTPUT);
  pinMode(DIR3pin, OUTPUT);

  ledcWrite(PWM1channel,0); // pwm channel, speed 0-255
  digitalWrite(DIR1pin, LOW); // set direction to cw/ccw

  ledcWrite(PWM2channel,0); // pwm channel, speed 0-255
  digitalWrite(DIR2pin, LOW); // set direction to cw/ccw

  ledcWrite(PWM3channel,0); // pwm channel, speed 0-255
  digitalWrite(DIR3pin, LOW); // set direction to cw/ccw


  
  //LASER INITIALIZATION
  pinMode(LASER_1, OUTPUT);
  digitalWrite(LASER_1, HIGH);
  pinMode(LASER_2, OUTPUT);
  digitalWrite(LASER_2, HIGH);
  
  Wire.begin();
  Wire.setClock(400000);

  LIDAR.setTimeout(500);
  if (!LIDAR.init()) {
    Serial.println("LIDAR 1 initialization failed");
    //while(1);
  }
  LIDAR.setDistanceMode(VL53L1X::Long);
  LIDAR.setMeasurementTimingBudget(33000);
  LIDAR.startContinuous(33);

  
}

void loop() {
  char c = 0;
  int an = 0;
  int i;
  int LIDAR_RANGE;
  int PT_1_VOLTAGE;
  int PT_2_VOLTAGE;

  
  
  if (Serial.available()) {
    SerialBT.write(Serial.read());
  }
  if (SerialBT.available()) {
    //Serial.write(SerialBT.read());
    c = SerialBT.read();
    if(c == 'o'){
      //digitalWrite(13,HIGH);
    }
    else if (c == 'p'){
      //digitalWrite(13,LOW);
    }
    else if (c == 'a'){
      an = analogRead(A2);
      SerialBT.print("a ");
      SerialBT.println(an);
    }
    else if (c == 'x'){
      count = count + 1;
      for (i=0; i<100; i++){
        SerialBT.print("x ");
        SerialBT.print(i);
        SerialBT.print(" ");
        SerialBT.println(int(50*sin(2*3.14/50*i+count)));
      }
    }
    else if (c == 'c') {
      SerialBT.println("c 1");
    }
    else if (c == 'w') {
      digitalWrite(DIR1pin, LOW);
      ledcWrite(PWM1channel, 256);
      digitalWrite(DIR2pin, LOW);
      ledcWrite(PWM2channel, 256);
    }
    else if (c == 's') {
      digitalWrite(DIR1pin, HIGH);
      ledcWrite(PWM1channel, 256);
      
      digitalWrite(DIR2pin, HIGH);
      ledcWrite(PWM2channel, 256);
    }
    else if (c == 'b') {
      ledcWrite(PWM1channel, 0);
      ledcWrite(PWM2channel, 0);
      ledcWrite(PWM3channel, 0);
    }
    else if (c=='q') {
      digitalWrite(DIR3pin, LOW);
      ledcWrite(PWM3channel, 256);
    }
    else if (c == 'e') {
      digitalWrite(DIR3pin, HIGH);
      ledcWrite(PWM3channel, 256);
    }
    else if (c == 'r') {
      LIDAR_RANGE = LIDAR.readRangeContinuousMillimeters();
      SerialBT.print(LIDAR_RANGE);
      SerialBT.print(" ");
      PT_1_VOLTAGE = analogRead(A2);
      PT_2_VOLTAGE = analogRead(A3);
      SerialBT.print("LASER_1:");
      SerialBT.print(PT_1_VOLTAGE);
      SerialBT.print(" ");
      SerialBT.print("LASER_2:");
      SerialBT.println(PT_2_VOLTAGE);
    }
  }
  delay(20);
}
