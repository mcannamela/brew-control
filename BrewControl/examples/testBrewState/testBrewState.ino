#include <BrewState.h>


void setup()
{
  Serial.begin(9600);
  Serial.println("BEGIN SETUP");
  for (int i = 0; i < N_DPINS; i++) {
    if (!isPinReserved(i)) {
      pinMode(i, OUTPUT);
    }
  }
  Serial.println("END SETUP");
}

void writeByParity(bool evenState) {
  for (int i = 0; i < N_DPINS; i++) {
    if (!isPinReserved(i)) {
      if (i % 2 == 0) {
        digitalWrite(i, evenState);
      }
      else {
        digitalWrite(i, !evenState);
      }
    }
  }
}

void printName(char* nm) {
  Serial.print("\n");
  Serial.print(nm);
  Serial.print(": ");
}

void printBoolArr(char* nm, bool* arr, int n) {
  printName(nm);
  Serial.print("len=");
  Serial.print(n);
  Serial.print(": ");
  for (int i = 0; i < n; i++) {
    Serial.print(arr[i]);
    Serial.print(", ");
  }
}


void loop()
{

  Serial.println("\n\nLOOP");
  bool digitalState[N_DPINS];
  for (int i=0; i<N_DPINS; i++){
    digitalState[i] = false;
  }
  printBoolArr("Init all false:             ", digitalState, N_DPINS); 
  
  delay(10);
  writeByParity(true);
  readDigitalState(digitalState);
  printBoolArr("Evens true if not reserved: ", digitalState, N_DPINS);
  
  delay(10);
  writeByParity(false);
  readDigitalState(digitalState);
  printBoolArr("Evens false if not reserved:", digitalState, N_DPINS);
  
  delay(2000);
}

