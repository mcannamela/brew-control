/*
 * enter one of the following USLs into your browser.
 * Replace "host" with the IP address assigned to the Arduino.
 *
 * http://host/
 * http://host/index.html
 *
 * These show help for using the rest of the server.
 * 
 * 
 * http://host/state.json
 *
 * This returns the state of the arguino as a json object
 * 
 * 
 * http://host/pincommand?command=#&othercommand=#
 *
 * This sends commands to the pins named in the query params and returns the status of the command
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
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println("BEGIN SETUP");
  
  /* initialize the Ethernet adapter */
  Ethernet.begin(mac, ip);
  tareLastInterruptTimes();
  delay(100);
  decayMeanInterruptTimes();

  /* setup our default command that will be run when the user accesses
   * the root page on the server */
  webserver.setDefaultCommand(&indexCmd);

  /* setup our default command that will be run when the user accesses
   * a page NOT on the server */
  webserver.setFailureCommand(&my_failCmd);

  /* run the same command if you try to load /index.html, a common
   * default page name */
  webserver.addCommand("index.html", &indexCmd);

  /*This command  is called if you try to load /raw.html */
  webserver.addCommand("state.json", &stateCmd);
  webserver.addCommand("pincommand", &pinCmd);

  /* start the webserver */
  webserver.begin();
  
  Serial.println("END SETUP");
}




void loop()
{
  char buff[128];
  int buff_len = 128;
  /* process incoming connections one at a time forever */
  webserver.processConnection(buff, &buff_len);
  decayMeanInterruptTimes();
  
}
