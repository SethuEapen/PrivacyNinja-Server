/*
* Arduino Wireless Communication Tutorial
*       Example 1 - Receiver Code
*                
* by Dejan Nedelkovski, www.HowToMechatronics.com
* 
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#define led 10

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";
boolean var = 0;
void setup() {
  pinMode(10, OUTPUT);
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MAX);
}
void loop() {
  radio.startListening();
  if (radio.available()) {
    radio.read(&var,sizeof(var));
    Serial.println(var);
    if(var == 1){
      digitalWrite(led, HIGH);
    }
    else {
      digitalWrite(led, LOW);
    }
   
  }
}
