#include <Interrupts.h>

void setup()
{
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println("BEGIN SETUP");
  pinMode(LED_PIN, OUTPUT);
  initInterruptTimeArrays();
  pinMode(INTERRUPT_PINS[0], OUTPUT);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PINS[0]), handleInterruptZero, RISING);
  Serial.println("END SETUP");
}


void testInterruptsUsingExternalSource(){
  Serial.println("EXTERNAL TEST INTERRUPTS");
  initInterruptTimeArrays();
  tareLastInterruptTimes();
  pinMode(INTERRUPT_PINS[0], INPUT);

  delay(3000);
  Serial.print("    Mean interrupt time: ");
  Serial.println(getMeanInterruptTime(0));
}


void loop()
{
  Serial.println("\n\nLOOP");
  delay(10);
  digitalWrite(LED_PIN, HIGH);
  testInterruptsUsingExternalSource();
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}
