#include "Constants.h"

#ifndef INTERRUPTS_H
#define INTERRUPTS_H

volatile unsigned long _LAST_INTERRUPT_TIME[N_INTERRUPT_PINS];
volatile double _MEAN_INTERRUPT_TIME[N_INTERRUPT_PINS];
const double _DECAY_WEIGHT = .95;


void initInterruptTimeArrays() {
  for (int i = 0; i < N_INTERRUPT_PINS; i) {
    _LAST_INTERRUPT_TIME[i] = 0;
    _MEAN_INTERRUPT_TIME[i] = 0.0;
  }
}


double updateAverage(double previousAverage, double thisPoint) {
  return _DECAY_WEIGHT * previousAverage + (1.0 - _DECAY_WEIGHT) * thisPoint;
}



void handleInterrupt(int interruptNr) {
  unsigned long t = millis();
  unsigned long delta;

  // only update if the clock has not overflowed
  if (t >= _LAST_INTERRUPT_TIME[interruptNr]) {
    delta = t - _LAST_INTERRUPT_TIME[interruptNr];
    _MEAN_INTERRUPT_TIME[interruptNr] = updateAverage(_MEAN_INTERRUPT_TIME[interruptNr], (double) delta);
  }
  
  _LAST_INTERRUPT_TIME[interruptNr] = t;
}


void handleInterruptZero() {
  handleInterrupt(0);
}

void handleInterruptOne() {
  handleInterrupt(1);
}

#endif
