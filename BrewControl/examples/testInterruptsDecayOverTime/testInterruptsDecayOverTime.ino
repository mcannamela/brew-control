#include <Interrupts.h>

void setup()
{
  Serial.begin(115200);
  Serial.println("BEGIN SETUP");
  pinMode(LED_PIN, OUTPUT);
  initInterruptTimeArrays();
  pinMode(INTERRUPT_PINS[0], OUTPUT);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PINS[0]), handleInterruptZero, INTERRUPT_TRIGGER);
  pulseInterruptRising(0, 1000);
  Serial.println("END SETUP");
}

void loop()
{
  Serial.println("\n\nLOOP");
  delay(10);
  digitalWrite(LED_PIN, HIGH);
  updateMeanInterruptTime(0,millis());
  Serial.print("Mean interrupt time after ");
  Serial.print(millis());
  Serial.print(": ");
  Serial.println(getMeanInterruptTime(0));
  delay(250);
}
