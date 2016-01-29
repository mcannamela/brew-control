#include <Interrupts.h>

void setup()
{
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println("BEGIN SETUP");
  pinMode(LED_PIN, OUTPUT);
  initInterruptTimeArrays();
  pinMode(INTERRUPT_PINS[0], OUTPUT);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PINS[0]), handleInterruptZero, INTERRUPT_TRIGGER);
  Serial.println("END SETUP");
}


void testInterruptsUsingDigitalWrite(){
  Serial.println("SELF TEST INTERRUPTS");
  initInterruptTimeArrays();
  tareLastInterruptTimes();
  pinMode(INTERRUPT_PINS[0], OUTPUT);
  for (int i=0; i<100; i++){
    pulseInterruptRising(0, random(5,15));
  }
  Serial.print("    Mean interrupt time: ");
  Serial.println(getMeanInterruptTime(0));
}


void loop()
{
  Serial.println("\n\nLOOP");
  delay(10);
  digitalWrite(LED_PIN, HIGH);
  testInterruptsUsingDigitalWrite();
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}
