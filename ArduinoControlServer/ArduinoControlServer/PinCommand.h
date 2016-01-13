#include "Constants.h"

bool areCommandsEqual(char* commandName, const char* constCommandName) { 
  
  char constCommandBuffer[NAMELEN];
  char commandBuffer[NAMELEN];
  
  PString constCommand(constCommandBuffer, NAMELEN);
  PString command(commandBuffer, NAMELEN);

  constCommand.print(constCommandName);
  command.print(commandName);

  return command == constCommand;
  

}


int executeCommand(char* commandName, char* value) {
  int pinNr = atoi(value);
  

  if (isPinReserved(pinNr)) {
    return FAIL_PIN_RESERVED;
  }
  else if (areCommandsEqual(commandName, SET_PINMODE_OUT)) {
    pinMode(pinNr, OUTPUT);
  }
  else if (areCommandsEqual(commandName, SET_PINMODE_IN)) {
    pinMode(pinNr, INPUT);
  }
  else if (areCommandsEqual(commandName, SET_PIN_HIGH)) {
    digitalWrite(pinNr, HIGH);
  }
  else if (areCommandsEqual(commandName, SET_PIN_LOW)) {
    digitalWrite(pinNr, LOW);
  }

  return COMMAND_OK;

}


