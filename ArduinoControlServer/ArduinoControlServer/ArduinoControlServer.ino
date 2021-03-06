
/* Web_Parms_1.pde - very simple Webduino example of parameter passing and parsing */

/*
 * This is mostly a tool for testing and debugging the library, but can
 * also be used as an example of coding for it.
 *
 * To use it,  enter one of the following USLs into your browser.
 * Replace "host" with the IP address assigned to the Arduino.
 *
 * http://host/
 * http://host/index.html
 *
 * These return a "success" HTTP result and display the parameters
 * (if any) passed to them as a single string,  without attempting to
 * parse them.  This is done with a call to defaultCmd.
 * 
 * 
 * http://host/raw.html
 *
 * This is essentially the same as the index.html URL processing,
 * but is done by calling rawCmd.
 * 
 * 
 * http://host/parsed.html
 *
 * This invokes parsedCmd,  which displays the "raw" parameter string,
 * but also uses the "nexyURLparam" routine to parse out the individual
 * parameters, and display them.
 */

#define WEBDUINO_SERIAL_DEBUGGING 1
#define WEBDUINO_FAIL_MESSAGE "<h1>Request Failed</h1>"
#include "SPI.h" // new include
#include "avr/pgmspace.h" // new include
#include "Ethernet.h"
#include <WebServer.h>

//#include "BrewControl.h"
#include "PinCommand.h"
#include "Interrupts.h"
#include "Requests.h"



/* copy-pasta from brewControlServer
byte mac[] = { 
  0x00, 0xAA, 0xBB, 0xCC, 0xDE, 0x02 };
IPAddress ip(192,168,11, 101);
IPAddress gateway(192,168,1, 1);
IPAddress subnet(255, 255, 255, 0);
*/


/* CHANGE THIS TO YOUR OWN UNIQUE VALUE.  The MAC number should be
 * different from any other devices on your network or you'll have
 * problems receiving packets. */
static uint8_t mac[] = { 0x00, 0xAA, 0xBB, 0xCC, 0xDE, 0x02 };


/* CHANGE THIS TO MATCH YOUR HOST NETWORK.  Most home networks are in
 * the 192.168.0.XXX or 192.168.1.XXX subrange.  Pick an address
 * that's not in use and isn't going to be automatically allocated by
 * DHCP from your router. */
static uint8_t ip[] = { 192, 168, 11, 101 };





/* This creates an instance of the webserver.  By specifying a prefix
 * of "", all pages will be at the root of the server. */
#define PREFIX ""
WebServer webserver(PREFIX, 80);



void setup()
{
  Serial.begin(9600);
  Serial.println("BEGIN SETUP");
  
  /* initialize the Ethernet adapter */
//  Ethernet.begin(mac, ip);

  /* setup our default command that will be run when the user accesses
   * the root page on the server */
  webserver.setDefaultCommand(&helloCmd);

  /* setup our default command that will be run when the user accesses
   * a page NOT on the server */
  webserver.setFailureCommand(&my_failCmd);

  /* run the same command if you try to load /index.html, a common
   * default page name */
  webserver.addCommand("index.html", &helloCmd);

  /*This command  is called if you try to load /raw.html */
  webserver.addCommand("raw.html", &rawCmd);
  webserver.addCommand("parsed.html", &parsedCmd);

  /* start the webserver */
//  webserver.begin();
  

  initInterruptTimeArrays();
  pinMode(INTERRUPT_PINS[0], OUTPUT);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PINS[0]), handleInterruptZero, RISING);
  Serial.println("END SETUP");
}

void testPinCommands(){
  char buff[64];
  int len = 64;

  char valbuff[32];
  valbuff[0] = '0';
  valbuff[1] = '9';
  valbuff[2] = '\0';
 

  PString command(buff, len);

  command.begin();
  command.print(SET_PINMODE_IN);
  Serial.println(command);
  executeCommand(command, valbuff);
  delay(100);

  command.begin();
  command.print(SET_PINMODE_OUT);
  Serial.println(command);
  executeCommand(command, valbuff);
  delay(100);

  command.begin();
  command.print(SET_PIN_HIGH);
  Serial.println(command);
  executeCommand(command, valbuff);
  delay(500);

  command.begin();
  command.print(SET_PIN_LOW);
  Serial.println(command);
  executeCommand(command, valbuff);
  delay(100);

  
  
}

void testInterruptsUsingDigitalWrite(){
  Serial.println("SELF TEST INTERRUPTS");
  initInterruptTimeArrays();
  tareLastInterruptTimes();
  pinMode(INTERRUPT_PINS[0], OUTPUT);
  for (int i=0; i<100; i++){
    pulseInterruptRising(0, random(5,15));
  }
  Serial.print("    Mean interrupt time: ");
  Serial.println(getMeanInterruptTime(0));
}

void testInterruptsUsingExternalSource(){
  Serial.println("EXTERNAL TEST INTERRUPTS");
  initInterruptTimeArrays();
  tareLastInterruptTimes();
  pinMode(INTERRUPT_PINS[0], INPUT);

  delay(3000);
  Serial.print("    Mean interrupt time: ");
  Serial.println(getMeanInterruptTime(0));
}

void loop()
{
  
  Serial.println("\n\nLOOP");
  delay(10);
  
  testPinCommands();
  testInterruptsUsingDigitalWrite();
  testInterruptsUsingExternalSource();
  
  delay(1000);

 
  /* process incoming connections one at a time forever */
  //webserver.processConnection(buff, &len);
}
