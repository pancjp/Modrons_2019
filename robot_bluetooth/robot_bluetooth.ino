#include <BluetoothSerial.h>
#include "BluetoothSerial.h"
#include <stdio.h>
#include <math.h>

BluetoothSerial SerialBT;

int count = 0;
const int PWM1pin = 14;
const int DIR1pin = 32;
const int PWM1channel = 0;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("A R N I E"); //Bluetooth device name
  //Serial.println("The device started, now you can pair it with bluetooth!");
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);

  ledcSetup(PWM1channel,5000,8); // pwm channel, frequency, resolution in bits
  ledcAttachPin(PWM1pin,PWM1channel); // pin, pwm channel

  pinMode(DIR1pin,OUTPUT); // set direction pin to output

  ledcWrite(PWM1channel,0); // pwm channel, speed 0-255
  digitalWrite(DIR1pin, LOW); // set direction to cw/ccw
}

void loop() {
  char c = 0;
  int an = 0;
  int i;
  
  if (Serial.available()) {
    SerialBT.write(Serial.read());
  }
  if (SerialBT.available()) {
    //Serial.write(SerialBT.read());
    c = SerialBT.read();
    if(c == 'o'){
      digitalWrite(13,HIGH);
    }
    else if (c == 'p'){
      digitalWrite(13,LOW);
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
    }
    else if (c == 's') {
      digitalWrite(DIR1pin, HIGH);
      ledcWrite(PWM1channel, 256);
    }
    else if (c == 'b') {
      ledcWrite(PWM1channel, 0);
    }
  }
  delay(20);
}
