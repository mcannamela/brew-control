#
#include <PString.h>

#ifndef CONSTANTS_H
#define CONSTANTS_H


#define NAMELEN 32
#define VALUELEN 32

const char  SET_PINMODE_OUT[] = "SET_PINMODE_OUT";
const char  SET_PINMODE_IN[] = "SET_PINMODE_IN";


const char  SET_PIN_HIGH[] = "SET_PIN_HIGH";
const char  SET_PIN_LOW[] = "SET_PIN_LOW";

const int RESERVED_PINS[] = {2, 3, 10, 11, 12, 13};
const int N_RESERVED_PINS = 6;

const int INTERRUPT_PINS[] = {2, 3};
const int N_INTERRUPT_PINS = 2;


const int N_DPINS = 16;
const int N_APINS = 5;


enum COMMAND_RESULT {
  COMMAND_OK,
  FAIL_PIN_RESERVED,
};


bool isPinReserved(int pinNr) {
  for (int i = 0; i < N_RESERVED_PINS; i++) {
    if (pinNr == RESERVED_PINS[i]) {
      return true;
    }
  };
  return false;
}


bool isInterruptPin(int pinNr) {
  for (int i = 0; i < N_INTERRUPT_PINS; i++) {
    if (pinNr == INTERRUPT_PINS[i]) {
      return true;
    }
  };
  return false;
}

#endif /* CONSTANTS_H */









