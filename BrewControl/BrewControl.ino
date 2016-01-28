/*
   enter one of the following USLs into your browser.
   Replace "host" with the IP address assigned to the Arduino.

   http://host/
   http://host/index.html

   These show help for using the rest of the server.


   http://host/state.json

   This returns the state of the arguino as a json object


   http://host/pincommand?command=#&othercommand=#

   This sends commands to the pins named in the query params and returns the status of the command
*/

#define WEBDUINO_SERIAL_DEBUGGING 0
#define WEBDUINO_FAIL_MESSAGE "<h1>Request Failed</h1>"
#include <PString.h>
#include "SPI.h" // new include
#include "avr/pgmspace.h" // new include
#include "Ethernet.h"
#include <WebServer.h>
#include "Requests.h"
#include "Interrupts.h"


/* This creates an instance of the webserver.  By specifying a prefix
   of "", all pages will be at the root of the server. */
#define PREFIX ""
WebServer webserver(PREFIX, 80);



void setup()
{
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println("BEGIN SETUP");

  /* initialize the Ethernet adapter */
  Ethernet.begin(mac, ip);
  initInterruptTimeArrays();
  tareLastInterruptTimes();
  delay(100);

  pinMode(INTERRUPT_PINS[0], INPUT);
  attachInterrupt(
    digitalPinToInterrupt(INTERRUPT_PINS[0]),
    handleInterruptZero,
    INTERRUPT_TRIGGER
  );

  /*pinMode(INTERRUPT_PINS[1], OUTPUT);
  attachInterrupt(
    digitalPinToInterrupt(INTERRUPT_PINS[1]),
    handleInterruptOne,
    INTERRUPT_TRIGGER
  );*/

  decayMeanInterruptTimes();

  /* setup our default command that will be run when the user accesses
     the root page on the server */
  webserver.setDefaultCommand(&indexCmd);
  webserver.addCommand("index.html", &indexCmd);

  webserver.addCommand("state.json", &stateCmd);
  webserver.addCommand("reserved.json", &reservedCmd);
  webserver.addCommand("pincommand", &pinCmd);

  /* setup our default command that will be run when the user accesses
     a page NOT on the server */
  webserver.setFailureCommand(&my_failCmd);

  /* start the webserver */
  webserver.begin();

  Serial.println("END SETUP");
}


unsigned long last_decay_time = 0;
unsigned long decay_interval = 1000;
bool should_decay_and_enforce_timeouts;

void loop()
{
  char buff[128];
  int buff_len = 128;
  
  
  /* process incoming connections one at a time forever */
  webserver.processConnection(buff, &buff_len);

  
  should_decay_and_enforce_timeouts = millis() > (last_decay_time + decay_interval);
  should_decay_and_enforce_timeouts = should_decay_and_enforce_timeouts || (millis() < last_decay_time);
  if ( should_decay_and_enforce_timeouts && false){
    Serial.println("Decay interrupts and enforce timeouts");
    last_decay_time = millis();
    decayMeanInterruptTimes(); 
    //enforceTimeouts();
  }
  
}
