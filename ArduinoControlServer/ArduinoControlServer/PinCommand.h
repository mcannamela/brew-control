#include "Constants.h"


bool areCommandsEqual(PString command, const char* constCommandName) {
  char constCommandBuffer[NAMELEN];
  PString constCommand(constCommandBuffer, NAMELEN);
  
  constCommand.print(constCommandName);
  command.print(commandName);

  return command == constCommand;
}


int executeCommand(PString command, char* value) {
  int pinNr = atoi(value);


  if (isPinReserved(pinNr)) {
    return FAIL_PIN_RESERVED;
  }
  else if (areCommandsEqual(command, SET_PINMODE_OUT)) {
    pinMode(pinNr, OUTPUT);
  }
  else if (areCommandsEqual(command, SET_PINMODE_IN)) {
    pinMode(pinNr, INPUT);

    //ensure internal pullup is off
    digitalWrite(pinNr, LOW);
  }
  else if (areCommandsEqual(command, SET_PIN_HIGH)) {
    digitalWrite(pinNr, HIGH);
  }
  else if (areCommandsEqual(command, SET_PIN_LOW)) {
    digitalWrite(pinNr, LOW);
  }

  return COMMAND_OK;

}


