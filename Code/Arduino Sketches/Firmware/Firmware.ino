/*  Aircraft Data Logger
    Purpose: Firmware for aircraft data logger

    Written by: B. Brookes
    Supervisor: Dr P.A. Robertson
*/

// Include header files
#include <SD.h>
#include<SPI.h>
#include <Wire.h>
#include <Adafruit_GPS.h>
#include "SparkFunMPL3115A2.h"

// Define pins on the MCU
int rec        = 6;
int stable     = 5;
int RecSwitch  = 7;
int reading_no = 0;

//Global vaules
float SwitchValue;
float pressure;
float temperature;

// Globals Strings
String GPSFile;
String PressureFile;
String data;

// For denoting if first pass through the conditional loop
bool FirstPassFlag = true;

// Used for timing
unsigned long current_time  = 0;
unsigned long previous_time = 0;
unsigned long elasped_time  = 0;

MPL3115A2 PressureSensor;
File mySensorData;
void setup()
{
  // Flash to show it started up
  pinMode(rec, OUTPUT);
  pinMode(stable, OUTPUT);
  digitalWrite(stable, HIGH);
  delay(1000);
  digitalWrite(rec, HIGH);
  delay(1000);
  digitalWrite(stable, LOW);
  delay(1000);
  digitalWrite(rec, LOW);
  
  // Initlaise all sensors/LEDs
  initMKT3339();
  initMPL311A2();
  SD.begin(10);

  delay(500);
  digitalWrite(stable, LOW);
  delay(500);
  digitalWrite(stable, LOW);
}

void loop()
{
  SwitchValue = analogRead(RecSwitch);
  if (SwitchValue > 1000)
  {
    reading_no = 0;
    if (FirstPassFlag == true)
    {
      GPSFile      = generateFile("GPS");
      PressureFile = generateFile("PRE");
      FirstPassFlag = false;

      // Low tech way of waiting for a stable fix
      digitalWrite(rec, HIGH);
      delay(5000);
      digitalWrite(stable, HIGH);
      previous_time = millis();

    }
    while(SwitchValue > 1000)
    {
        if(elasped_time  <5000)
        {
            digitalWrite(stable, HIGH);           
        }
        else
        {
            digitalWrite(stable, LOW);    
        }
        
        current_time = millis();
        elasped_time = current_time - previous_time;
       
        pressure = readPressure();
        temperature = readTemp();
        Serial.println(temperature);
        mySensorData = SD.open(PressureFile, FILE_WRITE);
        mySensorData.print(reading_no);
        mySensorData.print(", ");
        mySensorData.print(pressure);
        mySensorData.print(", ");
        mySensorData.println(temperature);
        mySensorData.close();
        
        data = Serial.readStringUntil('$');
        mySensorData = SD.open(GPSFile, FILE_WRITE);
        mySensorData.print(reading_no);
        mySensorData.print(", ");
        mySensorData.println(data);
        mySensorData.close();

        reading_no++;
        
        SwitchValue = analogRead(RecSwitch);
    }
  }
  else
  {
    digitalWrite(rec, LOW);
    digitalWrite(stable, LOW);
    FirstPassFlag = true;
  }
}
