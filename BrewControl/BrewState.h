#ifndef BREW_STATE_H
#define BREW_STATE_H
#include "Constants.h"

unsigned long _LAST_WRITE_TIME[N_DPINS];

void initLastWriteTime() {
  for (int i = 0; i < N_DPINS; i++) {
    _LAST_WRITE_TIME[i] = 0;
  }
}

void setLastWriteTime(int pinNr, unsigned long t) {
  _LAST_WRITE_TIME[pinNr] = t;
}

unsigned long getLastWriteTime(int pinNr) {
  return _LAST_WRITE_TIME[pinNr];
}

bool isTimedOut(int pinNr, unsigned long t) {
  unsigned long timeoutTime = getLastWriteTime(pinNr);
  return t > timeoutTime;
}

void readDigitalState(bool* state_out) {
  for (int i = 0; i < N_DPINS; i++) {
    state_out[i] = digitalRead(i);
  }
}


double getMeanAnalogValue(int pinNr) {
  double meanVal = 0.0;
  int val;
  for (int i = 0; i < N_ADC_READS; i++) {
    val = analogRead(pinNr);
    if (val == 0) {
      val++;
    }
    meanVal += (double) val;
  }
  meanVal /= (double) N_ADC_READS;
  return meanVal;
}


void readAnalogState(double* state_out) {
  for (int i = 0; i < N_APINS; i++) {
    state_out[i] = getMeanAnalogValue(i);
  }
}

#endif //BREW_STATE_H

