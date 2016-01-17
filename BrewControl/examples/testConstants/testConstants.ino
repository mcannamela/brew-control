#include <Constants.h>


void printName(char* nm) {
  Serial.print("\n");
  Serial.print(nm);
  Serial.print(": ");
}

void printCString(char* nm, const char* str) {
  printName(nm);
  Serial.println(str);
}

void printInt(char* nm, int n) {
  printName(nm);
  
  Serial.println(n);
}
void printULong(char* nm, unsigned long n) {
  printName(nm);
  Serial.println(n);
}

void printIntArr(char* nm, const int* arr, int n) {
  printName(nm);
  Serial.print("len=");
  Serial.print(n);
  Serial.print(": ");
  for (int i = 0; i < n; i++) {
    Serial.print(arr[i]);
    Serial.print(", ");
  }
}

void testIsPinReserved() {
  Serial.println("\nTest isPinReserved");
  for (int i = 0; i < N_RESERVED_PINS; i++) {
    if (isPinReserved(RESERVED_PINS[i])) {
      Serial.print("Pin ");
      Serial.print(RESERVED_PINS[i]);
      Serial.println(" reserved, OK");
    }
    else {
      Serial.print("Pin ");
      Serial.print(RESERVED_PINS[i]);
      Serial.println(" not reserved, FAIL");
    }

  }
}

void testLEDPinNotReserved() {
  Serial.println("\nTest LED_PIN is not reserved");
  if (isPinReserved(LED_PIN)) {
  Serial.print("Pin ");
    Serial.print(LED_PIN);
    Serial.println("reserved, FAIL");
  }
  else {
    Serial.print("Pin ");
    Serial.print(LED_PIN);
    Serial.println(" not reserved, OK");
  }
}

void testIsInterruptPin() {
  Serial.println("\nTest isInterruptPin");
  for (int i = 0; i < N_INTERRUPT_PINS; i++) {
    if (isPinReserved(INTERRUPT_PINS[i])) {
      Serial.print("Pin ");
      Serial.print(INTERRUPT_PINS[i]);
      Serial.println(" is interrupt, OK");
    }
    else {
      Serial.print("Pin ");
      Serial.print(INTERRUPT_PINS[i]);
      Serial.println(" not interrupt, FAIL");
    }

  }
}

void testLEDPinNotInterrup() {
  Serial.println("\nTest LED_PIN is not interrupt");
  if (isInterruptPin(LED_PIN)) {
  Serial.print("Pin ");
    Serial.print(LED_PIN);
    Serial.println(" is interrupt, FAIL");
  }
  else {
    Serial.print("Pin ");
    Serial.print(LED_PIN);
    Serial.println(" not interrupt, OK");
  }
}



void setup()
{
  Serial.begin(9600);
  Serial.println("BEGIN SETUP");
  pinMode(LED_PIN, OUTPUT);
  Serial.println("END SETUP");
}



void loop()
{

  Serial.println("\n\nLOOP");
  delay(10);
  digitalWrite(LED_PIN, HIGH);

  printInt("NAMELEN", NAMELEN);

  printInt("VALUELEN", VALUELEN);
  printInt("N_ADC_READS", N_ADC_READS);
  printInt("N_DPINS", N_DPINS);
  printInt("N_APINS", N_APINS);

  printULong("MAX_LONG", MAX_LONG);

  printCString("SET_PINMODE_OUT", SET_PINMODE_OUT);
  printCString("SET_PINMODE_IN", SET_PINMODE_IN);
  printCString("SET_PIN_HIGH", SET_PIN_HIGH);
  printCString("SET_PIN_LOW", SET_PIN_LOW);

  printIntArr("RESERVED_PINS", RESERVED_PINS, N_RESERVED_PINS);

  printIntArr("INTERRUPT_PINS", INTERRUPT_PINS, N_INTERRUPT_PINS);

  printInt("LED_PIN", LED_PIN);

  printULong("INTERLOCK_TIMEOUT", INTERLOCK_TIMEOUT);


  testIsPinReserved();
  testLEDPinNotReserved();

  testIsInterruptPin();
  testLEDPinNotInterrup();
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(2000);
}

