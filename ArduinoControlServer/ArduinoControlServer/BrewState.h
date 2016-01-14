#include "Constants.h"
#ifndef BREW_STATE_H
#define BREW_STATE_H

void readDigitalState(bool* state_out){
  for (int i=0; i<N_DIGITAL_PINS){
    state_out[i] = digitalRead(i)==HIGH;
  } 
}

double getMeanAnalogValue(int pinNr){
    double meanVal = 0.0;
    int val;
    for(int i=0; i<N_ADC_READS; i++){
        val = analogRead(pinNr);
        if (val==0){
            val++;
        }
        meanVal+= (double) val;
    }
    meanVal /= n_adc_reads;
        return meanVal;
}

void readAnalogState(double* state_out){
  for (int i=0; i<N_ANALOG_PINS){
    state_out[i] = getMeanAnalogValue(i);
  }
}

#endif //BREW_STATE_H

