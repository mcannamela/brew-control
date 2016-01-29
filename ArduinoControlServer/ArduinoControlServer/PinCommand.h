#include "Constants.h"

#ifndef PIN_COMMANDS_H
#define PIN_COMMANDS_H

bool areCommandsEqual(PString command, const char* constCommandName) {
  char constCommandBuffer[NAMELEN];
  PString constCommand(constCommandBuffer, NAMELEN);
  
  constCommand.print(constCommandName);

  return command == constCommand;
}


int executeCommand(PString command, char* value) {
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
    Serial.print("set pin high ");
    Serial.println(pinNr);
    digitalWrite(pinNr, HIGH);
  }
  else if (areCommandsEqual(command, SET_PIN_LOW)) {
    Serial.print("set pin low  ");
    Serial.println(pinNr);
    digitalWrite(pinNr, LOW);
  }
  Serial.println("");

  return COMMAND_OK;

}

#endif

