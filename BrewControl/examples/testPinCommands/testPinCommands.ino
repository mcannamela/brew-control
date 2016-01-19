#include <PinCommand.h>


void setup()
{
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println("BEGIN SETUP");
  
  Serial.println("END SETUP");
}

void testPinCommands(){
  char buff[64];
  int len = 64;

  char valbuff[32];
  valbuff[0] = '0';
  valbuff[1] = '9';
  valbuff[2] = '\0';
 

  PString command(buff, len);

  command.begin();
  command.print(SET_PINMODE_IN);
  Serial.println(command);
  executeCommand(command, valbuff);
  delay(100);

  command.begin();
  command.print(SET_PINMODE_OUT);
  Serial.println(command);
  executeCommand(command, valbuff);
  delay(100);

  command.begin();
  command.print(SET_PIN_HIGH);
  Serial.println(command);
  executeCommand(command, valbuff);
  delay(500);

  command.begin();
  command.print(SET_PIN_LOW);
  Serial.println(command);
  executeCommand(command, valbuff);
  delay(100);

  
  
}


void loop()
{
  
  Serial.println("\n\nLOOP");
  delay(10);
  
  testPinCommands();
  
  delay(1000);
}
