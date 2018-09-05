#include <LiquidCrystal.h>

int counter = 1;
// NOTE!!! Don't use the pins 0 - 1 when interfacing with the lcd because it interrupts with the serial monitor
LiquidCrystal lcd(2,3,8,9,10,11);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Start of serial monitor");
  Serial.println("------ START OF LOOP ------");
  /*
  lcd.begin(16, 2);
  lcd.setCursor(0,0);
  lcd.print("Actual");
  lcd.setCursor(0,1);
  lcd.print("Moisture");
  */
  lcd.begin(16,2);
  lcd.setCursor(0,0);
  lcd.print("Hello");
  lcd.setCursor(0,1);
  lcd.print("World");
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  Serial.println("Loop number: " + String(counter));
  counter++;
  delay(1000);
  */
  int sensorValue = analogRead(A0);
  Serial.println(sensorValue);
  lcd.begin(16,2);
  lcd.setCursor(0,0);
  lcd.print("Sensor value");
  lcd.setCursor(0,1);
  lcd.print(sensorValue);
  delay(1000);
  /*
  float soilMoisture = analogRead(A0);
  lcd.setCursor(9,0);
  lcd.print(soilMoisture);
  soilMoisture = constrain(soilMoisture, 0, 200);
  soilMoisture = map(soilMoisture, 200, 0, 100, 0);
  lcd.setCursor(8, 1);
  lcd.print((String)soilMoisture+" %");
  Serial.println((String)soilMoisture + " %");
  delay(1000);
  */
}

