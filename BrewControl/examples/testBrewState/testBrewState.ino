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


void printDoubleArr(char* nm, double* arr, int n) {
  printName(nm);
  Serial.print("len=");
  Serial.print(n);
  Serial.print(": ");
  for (int i = 0; i < n; i++) {
    Serial.print(arr[i]);
    Serial.print(", ");
  }
}

void testTimeoutFunctions(){

  unsigned long writeTime=1001; 
  unsigned long timeoutTime = writeTime + INTERLOCK_TIMEOUT + 1;
  unsigned long notTimeoutTime = writeTime + INTERLOCK_TIMEOUT + 1;


  setLastWriteTime(LED_PIN, writeTime);
  Serial.print("Last write time should be :");
  Serial.println(writeTime);
  Serial.print("And it is: ");
  Serial.println(getLastWriteTime(LED_PIN));

  if (isTimedOut(LED_PIN, timeoutTime)){
    Serial.print("Timed out at ");
    Serial.print(timeoutTime);
    Serial.print(", OK");
  }
  else {
    Serial.print("Not timed out at ");
    Serial.print(timeoutTime);
    Serial.print(", FAIL");
  }

  if (!isTimedOut(LED_PIN, notTimeoutTime)){
    Serial.print("Not timed out at ");
    Serial.print(notTimeoutTime);
    Serial.print(", OK");
  }
  else {
    Serial.print("Timed out at ");
    Serial.print(notTimeoutTime);
    Serial.print(", FAIL");
  }

}



void loop()
{

  Serial.println("\n\nLOOP");
  double analogState[N_APINS];
  for (int i=0; i<N_APINS; i++){
    analogState[i] = 0.0;
  }
  
  bool digitalState[N_DPINS];
  for (int i=0; i<N_DPINS; i++){
    digitalState[i] = false;
  }

  Serial.println("\nREAD DIGITAL STATE");
  printBoolArr("Init all false:             ", digitalState, N_DPINS); 
  
  delay(10);
  writeByParity(true);
  readDigitalState(digitalState);
  printBoolArr("Evens true if not reserved: ", digitalState, N_DPINS);
  
  delay(10);
  writeByParity(false);
  readDigitalState(digitalState);
  printBoolArr("Evens false if not reserved:", digitalState, N_DPINS);

  delay(300);
  Serial.println("\n\nREAD ANALOG STATE");
  printDoubleArr("Init all 0.0:     ", analogState, N_APINS); 
  
  delay(10);
  readAnalogState(analogState);
  printDoubleArr("Behold the noise: ", analogState, N_APINS); 

  
  
  delay(2000);
}

