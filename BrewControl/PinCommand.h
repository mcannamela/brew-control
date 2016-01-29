#ifndef PIN_COMMANDS_H
#define PIN_COMMANDS_H
#include "Arduino.h"
#include "Constants.h"
#include "BrewState.h"



bool areCommandsEqual(PString command, const char* constCommandName) {
  char constCommandBuffer[NAMELEN];
  PString constCommand(constCommandBuffer, NAMELEN);

  constCommand.print(constCommandName);

  return command == constCommand;
}

void setPinLow(int pinNr) {
  Serial.print("set pin LOW  ");
  Serial.println(pinNr);
  digitalWrite(pinNr, LOW);
  setLastWriteTime(pinNr, millis());
}

void setPinHigh(int pinNr) {
  Serial.print("   set pin HIGH ");
  Serial.println(pinNr);
  digitalWrite(pinNr, HIGH);
  setLastWriteTime(pinNr, millis());
}

COMMAND_RESULT executeCommand(PString command, char* value) {
  Serial.print("executeCommand( ");
  Serial.print(command);
  Serial.print(", ");
  Serial.print(value);
  Serial.print("-->)");

  int pinNr = atoi(value);
  Serial.println(pinNr);

  if (isPinReserved(pinNr)) {
    Serial.println("Fail, pin is reserved.");
    Serial.println("");
    return FAIL_PIN_RESERVED;
  }
  else if (areCommandsEqual(command, SET_PINMODE_OUT)) {
    Serial.print("set pinmode out ");
    Serial.println(pinNr);
    pinMode(pinNr, OUTPUT);
  }
  else if (areCommandsEqual(command, SET_PINMODE_IN)) {
    Serial.print("set pinmode in ");
    Serial.println(pinNr);

    pinMode(pinNr, INPUT);

    //ensure internal pullup is off
    digitalWrite(pinNr, LOW);
  }
  else if (areCommandsEqual(command, SET_PIN_HIGH)) {
    setPinHigh(pinNr);
  }
  else if (areCommandsEqual(command, SET_PIN_LOW)) {
    setPinLow(pinNr);
  }
  else{
    Serial.println("Fail, unknown command.");
    Serial.println("");
    return UNKNOWN_COMMAND;
  }
  Serial.println("");

  return COMMAND_OK;

}

COMMAND_RESULT executeCommand(char* command, int commandLen, char* value){
  char buff[NAMELEN];
  int len = NAMELEN;
  COMMAND_RESULT retcode;

  PString pcommand(buff, len);
  pcommand.print(command);
  retcode = executeCommand(pcommand, value);
  return retcode;
}

int enforceTimeouts() {
  int nTimeouts = 0;
  unsigned long t = millis();
  Serial.println("\nenforceTimeouts");
  
  for (int i = 0; i < N_DPINS; i++) {
    if (!isPinReserved(i) && isTimedOut(i, t)) {
      setPinLow(i);
      nTimeouts++;
    }
  }
  return nTimeouts;
}

#endif

