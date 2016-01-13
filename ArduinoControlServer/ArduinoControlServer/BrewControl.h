#include "Constants.h"


const int hltActuatorPin = 7;
const int mashActuatorPin = 8;
const int fermenterActuatorPin = 9;

const int hltTemperaturePin = 0;
const int mashTemperaturePin = 1;
const int fermenterTemperaturePin = 2;

const double hltDividerResistance = 10000.0;
const double mashDividerResistance = 10000.0;
const double fermenterDividerResistance = 10000.0;


const int n_adc_reads = 32;



void setupBrewPins() {
  pinMode(hltActuatorPin, OUTPUT);
  pinMode(mashActuatorPin , OUTPUT);
  }
  
void actuateHeater(int pinNr){
    digitalWrite(pinNr, HIGH);
}

void deactuateHeater(int pinNr){
    digitalWrite(pinNr, LOW);
}

double readAdcValue(int pinNr){
    double meanVal = 0.0;
    int val;
    for(int i=0;i<n_adc_reads;i++){
        val = analogRead(pinNr);
        if (val==0){
            val++;
        }
        meanVal+= (double) val;
    }
    meanVal /= n_adc_reads;
        return meanVal;
}

double getDividerResistance(int pinNr){
    double dividerResistance;
    switch (pinNr){
          case hltTemperaturePin:
            dividerResistance=hltDividerResistance;
            break;
          case mashTemperaturePin:
            dividerResistance=mashDividerResistance;
            break;
          case fermenterTemperaturePin:
            dividerResistance=fermenterDividerResistance;
    }
    return dividerResistance;
}

double readThermistorResistance(int pinNr){
  double thermistorResistance;
  double dividerResistance = getDividerResistance(pinNr);
  double adcValue = readAdcValue(pinNr);
  
  thermistorResistance = dividerResistance/(1023.0/(adcValue) -1);
  return thermistorResistance;
}

double convertResistanceToTemperature(double thermistorResistance){
  double rT, t;
  rT = 1.0/298.15+(1.0/3950.0)*log(thermistorResistance/10000.0);
  t = 1.0/rT-273.15;
  return t;
}

double getTemperature(int pinNr){
    double thermistorResistance = readThermistorResistance(pinNr);
    double temperature = convertResistanceToTemperature(thermistorResistance);
    return temperature;
}

double getHltTemperature(){
    return getTemperature(hltTemperaturePin);
}

double getMashTemperature(){
    return getTemperature(mashTemperaturePin);
}

double getFermenterTemperature(){
    return getTemperature(fermenterTemperaturePin);
}

void actuateHltHeater(){
    actuateHeater(hltActuatorPin);
}

void actuateMashHeater(){
    actuateHeater(mashActuatorPin);
}

void deactuateHltHeater(){
    deactuateHeater(hltActuatorPin);
}
void deactuateMashHeater(){
    deactuateHeater(mashActuatorPin);
}
void deactuateFermenterHeater(){
    deactuateHeater(fermenterActuatorPin);
}

void deactuate(){
	deactuateHltHeater();
	deactuateMashHeater();
	deactuateFermenterHeater();
}



