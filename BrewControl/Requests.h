#ifndef REQUESTS_H
#define REQUESTS_H
#define VERSION_STRING "0.1"
#include <ArduinoJson.h>
#include "Constants.h"
#include "BrewState.h"
#include "Interrupts.h"

// ROM-based messages used by the application
// These are needed to avoid having the strings use up our limited
//    amount of RAM.

P(Page_start) = "<html><head><title>THIS IS BREW CONTROL " VERSION_STRING "</title></head><body>\n";
P(Page_end) = "</body></html>";

P(IndexHead) = "<h1>Welcome to BREW CONTROL</h1><br>\n";
P(IndexFail) = "Only handle GET and HEAD here.";

P(URLHelp) = "/state.json to read current state.<br>\n<br>\n /pincommand?command1=pin1&command1=pin2&command2=pin3 to set pin states.<br>\n<br>\nAvailable commands are: <br>\n";
P(TimeoutHelp_begin) = "Pins written HIGH will timeout after ";
P(ReservedPins_begin) = "Following pins are reserved and will not accept commands:";
P(InterruptPins_begin) = "Following pins will be monitored for external interrupts triggering on ";

P(Get_head) = "<h1>GET from ";
P(Post_head) = "<h1>POST to ";
P(Unknown_head) = "<h1>UNKNOWN request for ";
P(Default_head) = "unidentified URL requested.</h1><br>\n";
P(Raw_head) = "raw.html requested.</h1><br>\n";
P(Parsed_head) = "parsed.html requested.</h1><br>\n";
P(Good_tail_begin) = "URL tail = '";
P(Bad_tail_begin) = "INCOMPLETE URL tail = '";
P(Tail_end) = "'<br>\n";
P(Parsed_tail_begin) = "URL parameters:<br>\n";
P(Parsed_item_separator) = " = '";
P(Params_end) = "End of parameters<br>\n";
P(Post_params_begin) = "Parameters sent by POST:<br>\n";
P(Line_break) = "<br>\n";

/* commands are functions that get called by the webserver framework
   they can read any posted data from client, and they output to the
   server to send data back to the web browser. */
void indexCmd(WebServer &server, WebServer::ConnectionType type, char *url_tail, bool tail_complete)
{
  switch (type)
  {
    case WebServer::HEAD:
      server.httpSuccess();
      return;
    case WebServer::GET:
      server.httpSuccess();

      break;
    default:
      server.httpFail();
      server.printP(IndexFail);
      return;
  }

  server.printP(IndexHead);
  server.printP(URLHelp);

  server.print(SET_PINMODE_OUT);
  server.printP(Line_break);
  server.print(SET_PINMODE_IN);
  server.printP(Line_break);
  server.print(SET_PIN_HIGH);
  server.printP(Line_break);
  server.print(SET_PIN_LOW);
  server.printP(Line_break);
  server.printP(Line_break);

  server.printP(TimeoutHelp_begin);
  server.print(INTERLOCK_TIMEOUT);
  server.println(" ms");
  server.printP(Line_break);
  server.printP(Line_break);

  server.printP(ReservedPins_begin);
  for (int i = 0; i < N_RESERVED_PINS; i++) {
    server.printP(Line_break);
    server.print(RESERVED_PINS[i]);

  }
  server.printP(Line_break);
  server.printP(Line_break);

  server.printP(InterruptPins_begin);
  server.print(INTERRUPT_TRIGGER_NAME);
  server.print("=");
  server.print(INTERRUPT_TRIGGER);
  server.print(":");
  for (int i = 0; i < N_INTERRUPT_PINS; i++) {
    server.printP(Line_break);
    server.print(INTERRUPT_PINS[i]);

  }
  server.printP(Line_break);
  server.printP(Line_break);



  server.printP(Page_end);
}

void stateCmd(WebServer &server, WebServer::ConnectionType type, char *url_tail, bool tail_complete)
{
  Serial.println("getState");
  switch (type)
  {
    case WebServer::HEAD:
      server.httpSuccess();
      return;
    case WebServer::GET:
      server.httpSuccess();
      break;
    default:
      server.httpFail();
      server.printP(IndexFail);
      return;
  }

  Serial.println("Init state vars");
  bool digitalState[N_DPINS];
  double analogState[N_APINS];
  double meanInterruptTimes[N_INTERRUPT_PINS];
  StaticJsonBuffer<256> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  JsonArray& digital = root.createNestedArray("digital");
  JsonArray& analog = root.createNestedArray("analog");
  JsonArray& interrupt = root.createNestedArray("interrupt_periods");

  Serial.println("Read d");
  readDigitalState(digitalState);
  Serial.println("Read a");
//  readAnalogState(analogState);
  Serial.println("Read i");
  readMeanInterruptTimes(meanInterruptTimes);

  Serial.println("Encode d");
  //for (int i=0; i<N_DPINS; i++){
    //digital.add(digitalState[i]);
  //}

  Serial.println("Encode a");
  /*for (int i=0; i<N_APINS; i++){
    analog.add(analogState[i],6);
  }*/

  Serial.println("Encode i");
  for (int i=0; i<N_INTERRUPT_PINS; i++){
    interrupt.add(meanInterruptTimes[i], 6);
  }

  root.printTo(Serial);
  root.printTo(server);
}



void pinCmd(WebServer &server, WebServer::ConnectionType type, char *url_tail, bool tail_complete)
{
  URLPARAM_RESULT rc;
  char name[NAMELEN];
  char value[VALUELEN];

  /* this line sends the standard "we're all OK" headers back to the
     browser */
  server.httpSuccess();

  /* if we're handling a GET or POST, we can output our data here.
     For a HEAD request, we just stop after outputting headers. */
  if (type == WebServer::HEAD)
    return;

  server.printP(Page_start);
  switch (type)
  {
    case WebServer::GET:
      server.printP(Get_head);
      break;
    case WebServer::POST:
      server.printP(Post_head);
      break;
    default:
      server.printP(Unknown_head);
  }

  server.printP(Parsed_head);
  server.printP(tail_complete ? Good_tail_begin : Bad_tail_begin);
  server.print(url_tail);
  server.printP(Tail_end);

  if (strlen(url_tail))
  {
    server.printP(Parsed_tail_begin);
    while (strlen(url_tail))
    {
      rc = server.nextURLparam(&url_tail, name, NAMELEN, value, VALUELEN);
      if (rc == URLPARAM_EOS)
        server.printP(Params_end);
      else
      {
        server.print(name);
        server.printP(Parsed_item_separator);
        server.print(value);
        server.printP(Tail_end);
      }
    }
  }
  if (type == WebServer::POST)
  {
    server.printP(Post_params_begin);
    while (server.readPOSTparam(name, NAMELEN, value, VALUELEN))
    {
      server.print(name);
      server.printP(Parsed_item_separator);
      server.print(value);
      server.printP(Tail_end);
    }
  }
  server.printP(Page_end);

}

void my_failCmd(WebServer &server, WebServer::ConnectionType type, char *url_tail, bool tail_complete)
{
  /* this line sends the "HTTP 400 - Bad Request" headers back to the
     browser */
  server.httpFail();

  /* if we're handling a GET or POST, we can output our data here.
     For a HEAD request, we just stop after outputting headers. */
  if (type == WebServer::HEAD)
    return;

  server.printP(Page_start);
  switch (type)
  {
    case WebServer::GET:
      server.printP(Get_head);
      break;
    case WebServer::POST:
      server.printP(Post_head);
      break;
    default:
      server.printP(Unknown_head);
  }

  server.printP(Default_head);
  server.printP(tail_complete ? Good_tail_begin : Bad_tail_begin);
  server.print(url_tail);
  server.printP(Tail_end);
  server.printP(Page_end);

}

#endif

