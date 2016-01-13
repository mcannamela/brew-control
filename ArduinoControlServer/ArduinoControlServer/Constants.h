#include <PString.h>

#define NAMELEN 32
#define VALUELEN 32

const char  SET_PINMODE_OUT[] = "SET_PINMODE_OUT";
const char  SET_PINMODE_IN[] = "SET_PINMODE_IN";


const char  SET_PIN_HIGH[] = "SET_PIN_HIGH";
const char  SET_PIN_LOW[] = "SET_PIN_LOW";

const int RESERVED_PINS[] = {2, 3, 10, 11, 12, 13};
const int   RESERVED_PINS_LEN = 6;


enum COMMAND_RESULT {
  COMMAND_OK,
  FAIL_PIN_RESERVED,
};


bool isPinReserved(int pinNr) {
  for (int i = 0; i < RESERVED_PINS_LEN; i++) {
    if (pinNr == RESERVED_PINS[i]) {
      return true;
    }
  };
  return false;
}


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






