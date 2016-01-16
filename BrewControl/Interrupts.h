#ifndef INTERRUPTS_H
#define INTERRUPTS_H
#include "Arduino.h"
#include "Constants.h"


volatile unsigned long _LAST_INTERRUPT_TIME[N_INTERRUPT_PINS];
volatile double _MEAN_INTERRUPT_TIME[N_INTERRUPT_PINS];
const double _DECAY_WEIGHT = .95;


void initInterruptTimeArrays() {
  for (int i = 0; i < N_INTERRUPT_PINS; i++) {
    _LAST_INTERRUPT_TIME[i] = 0;
    _MEAN_INTERRUPT_TIME[i] = 0.0;
  }
}

void tareLastInterruptTimes(){
  unsigned long t = millis();
  for (int i = 0; i < N_INTERRUPT_PINS; i++) {
    _LAST_INTERRUPT_TIME[i] = t;
  }
}


double updateAverage(double previousAverage, double thisPoint) {
  return _DECAY_WEIGHT * previousAverage + (1.0 - _DECAY_WEIGHT) * thisPoint;
}


void updateMeanInterruptTime(int interruptNr, unsigned long t){
  unsigned long delta;

  // only update if the clock has not overflowed
  if (t >= _LAST_INTERRUPT_TIME[interruptNr]) {
    delta = t - _LAST_INTERRUPT_TIME[interruptNr];
    _MEAN_INTERRUPT_TIME[interruptNr] = updateAverage(_MEAN_INTERRUPT_TIME[interruptNr], (double) delta);
  }
  else{
    //ensure we fix the overflow
    _LAST_INTERRUPT_TIME[interruptNr] = t;
  }
}


void handleInterrupt(int interruptNr) {
   //toggle led for debugging
//  digitalWrite(LED_PIN, !digitalRead(LED_PIN));

  unsigned long t = millis();
  updateMeanInterruptTime(interruptNr, t);
  _LAST_INTERRUPT_TIME[interruptNr] = t;
}




void handleInterruptZero() {
  handleInterrupt(0);
}

void handleInterruptOne() {
  handleInterrupt(1);
}

void pulseInterruptRising(int interruptIndex, long pulseWidth) {
  _LAST_INTERRUPT_TIME[interruptIndex] = MAX_LONG;
  int pinNr = INTERRUPT_PINS[0];
  
  digitalWrite(pinNr, LOW);
  delay(1);
  digitalWrite(pinNr, HIGH);
  delay(1);
  digitalWrite(pinNr, LOW);
  delay(pulseWidth);
  digitalWrite(pinNr, HIGH);
}

double getMeanInterruptTime(int interruptIndex) {
  double t = _MEAN_INTERRUPT_TIME[interruptIndex];
  return t;
}

#endif
