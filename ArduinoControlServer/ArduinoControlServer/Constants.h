#
#include <PString.h>

#ifndef CONSTANTS_H
#define CONSTANTS_H


#define NAMELEN 32
#define VALUELEN 32
#define N_ADC_READS = 32

#define N_DPINS 16
#define N_APINS 5
#define MAX_LONG 4294967295


const char  SET_PINMODE_OUT[] = "SET_PINMODE_OUT";
const char  SET_PINMODE_IN[] = "SET_PINMODE_IN";


const char  SET_PIN_HIGH[] = "SET_PIN_HIGH";
const char  SET_PIN_LOW[] = "SET_PIN_LOW";

const int RESERVED_PINS[] = {2, 3, 10, 11, 12, 13};
const int N_RESERVED_PINS = 6;

const int INTERRUPT_PINS[] = {2, 3};
#define N_INTERRUPT_PINS 2

const int LED_PIN = 9;


enum COMMAND_RESULT {
  COMMAND_OK,
  FAIL_PIN_RESERVED,
};


bool isPinReserved(int pinNr) {
  Serial.print("isPinReserved(");
  Serial.print(pinNr);
  Serial.println(")");
  for (int i = 0; i < N_RESERVED_PINS; i++) {
    if (pinNr == RESERVED_PINS[i]) {
      Serial.print(pinNr);
      Serial.print("==RESERVED_PINS[");
      Serial.print(i);
      Serial.print("]<--");
      Serial.println(RESERVED_PINS[i]);
      return true;
    }
  };
  Serial.print(pinNr);
  Serial.println(" is not reserved");
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









