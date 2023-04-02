#include "Adafruit_Thermal.h"
#include "SoftwareSerial.h"
#include "bitmaps.h"
#include <Servo.h>

#define TX_PIN 16 // Arduino TX pin -- RX on printer
#define RX_PIN 17 // Arduino RX pin -- TX on printer

bool led; 
String quottie;
String emo; 
Servo myservo; 
int pos;

SoftwareSerial printer_comms(RX_PIN, TX_PIN);
Adafruit_Thermal printer(&printer_comms);


void printTermalQuote(String quote);
void printEmo(String emo);


void setup()
{  
  printer_comms.begin(19200);
  printer.begin();
  Serial.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);
  myservo.attach(2);

  printer.setHeatConfig(7,255,255);
}

void printTitle(){

  printer.feed(2);
  printer.doubleHeightOn();
  printer.println(F("The Galactic Mood Monitor"));
  printer.doubleHeightOff();
}

void printThermalQuote(String quote){
  
  printer.setFont('A');
  printer.println("");
  printer.doubleHeightOn();
  printer.println(F("Quote of The Day:"));
  printer.doubleHeightOff();

  printer.println(quote);
  printer.feed(2);


}

void printEmo(String emo){

  printer.setHeatConfig(21, 240, 20);

  printer.println(F("Your Daily Music Mix"));

  if(!emo.compareTo("happy")){
    printer.println("I got some upbeat tunes for you.");
    printer.printBitmap(QRCODEWH ,QRCODEWH ,HAPPYQRCODE);
  }
  else if(!emo.compareTo("sad")){
    printer.println("I got something a little somber for you.");
    printer.printBitmap(QRCODEWH ,QRCODEWH ,SADQRCODE);
  }
  else if(!emo.compareTo("neutral")){
    ("Heres something to get you through your day your day.");
    printer.printBitmap(QRCODEWH ,QRCODEWH ,NEUTRALQRCODE);
  }
  else{
    ("In case you want a throwback.");
    printer.printBitmap(QRCODEWH ,QRCODEWH ,RICKROLL);
  }
  printer.setDefault();
}

void loop() { 

    for (pos = 180; pos >= 30; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }

  if(Serial.readStringUntil('$').equals("%")){
    emo = Serial.readStringUntil('$');
    quottie = Serial.readStringUntil('$');

    Serial.print(emo);
    Serial.print(quottie);
    
    printer.justify('C');

    printTitle();
    printThermalQuote(quottie);
    printEmo(emo);

    
    //printer.printBitmap(360 ,303 ,Garf);
    printer.feed(2);

  }
  for (pos = 30; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  // printer.setDefault();

  // printer.printBitmap(360 ,303 ,Garf);
  // printer.feed(2);

}
