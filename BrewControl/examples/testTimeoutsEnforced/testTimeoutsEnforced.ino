#include <PinCommand.h>


void setup()
{
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println("BEGIN SETUP");

  Serial.println("END SETUP");
}

void printState() {
  Serial.print("The state is ");
  Serial.println(digitalRead(LED_PIN));
}

void testPinCommandsUpdateLastWriteTime() {
  char buff[64];
  int len = 64;
  PString command(buff, len);

  char valbuff[32];
  valbuff[0] = '0';
  valbuff[1] = '9';
  valbuff[2] = '\0';

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  initLastWriteTime();

  Serial.print("Last write time should be 0: ");
  Serial.println(getLastWriteTime(LED_PIN));

  unsigned long t0 = millis();

  command.begin();
  command.print(SET_PIN_HIGH);
  Serial.println(command);
  executeCommand(command, valbuff);

  Serial.print("Last write time should be close to (and surely more than)");
  Serial.print(t0);
  Serial.print(": ");
  Serial.println(getLastWriteTime(LED_PIN));
  printState();
  
  Serial.print("Will now delay for ");
  Serial.print( INTERLOCK_TIMEOUT / 2);
  Serial.println(", halfway to timeout...");
  delay(INTERLOCK_TIMEOUT / 2);
  
  Serial.println("...enforcing timeouts, pin should remain HIGH.");
  printState();
  Serial.print("Will now delay for ");
  Serial.print(10 + INTERLOCK_TIMEOUT / 2);
  Serial.println("s, until timed out...");
  delay(10 + INTERLOCK_TIMEOUT / 2);
  Serial.println("...thanks for your patience. Will now enforce timeouts, pin should go LOW");
  enforceTimeouts();
  printState();

  t0 = millis();
  
  command.begin();
  command.print(SET_PIN_LOW);
  Serial.println(command);
  executeCommand(command, valbuff);
  Serial.print("Last write time should be close to (and surely more than)");
  Serial.print(t0);
  Serial.print(": ");
  Serial.println(getLastWriteTime(LED_PIN));
}


void loop()
{

  Serial.println("\n\nLOOP");
  delay(10);

  testPinCommandsUpdateLastWriteTime();

  delay(1000);
}
