// Header files
#include <SD.h>
#include<SPI.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>


// Set up GPS serial
SoftwareSerial mySerial(11,10);
Adafruit_GPS GPS(&mySerial);

// Global variables
long startTime;
String NMEA1;
String NMEA2;
char c;      
float deg;
float degWhole;
float degDec;
int chipSelect = 53; 
unsigned long time;
int AnalogPin = 3;
int SwitchValue = 0;         
bool FirstPastFlag = true;
char GPSFile;
char PressureFile;
File mySensorData;

 // Main body ----------------------------------------------------------
void setup()
{
    GPS.begin(9600);
    Serial.begin(9600);  // start serial for output
   // Serial1.begin(9600);
    GPS.sendCommand("$PGCMD,33,0*6D");
    GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
    GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);      // 1Hz update rate
    delay(1000); 
  
    SD.begin(chipSelect);
    pinMode(8,OUTPUT);
}

void loop()
{
    
    SwitchValue = analogRead(AnalogPin);     // read the input pin
    if(SwitchValue > 600) //Only save data if switch on
    {
        Serial.println("In if");
        if(FirstPastFlag == true)
        {
            GPSFile      = generateFiles("GPS");
            PressureFile = generateFiles("Alt");
            FirstPastFlag = false;
        }
        
        digitalWrite(8,HIGH);                               // Turn LED ON
        // Save GPS data to SD card
        readGPS();  
        mySensorData = SD.open(GPSFile, FILE_WRITE); 
        mySensorData.println(NMEA1);
        mySensorData.println(NMEA2);
        mySensorData.close();
    
    }
    else
    {
        digitalWrite(8,LOW);
        delay(2000);
        FirstPastFlag = true;
    }
}

// Function Defintions -------------------------------------------------
void readGPS() 
{ 
    Serial.println("Sentence 1");
    clearGPS();   
    while(!GPS.newNMEAreceived()) 
    {
        c=GPS.read();
        Serial.println(c);
    }
    GPS.parse(GPS.lastNMEA());
    NMEA1=GPS.lastNMEA();

    Serial.println("Sentence 2");
    while(!GPS.newNMEAreceived()) 
    {
    c=GPS.read();
    }
    GPS.parse(GPS.lastNMEA());
    NMEA2=GPS.lastNMEA();

    Serial.println(NMEA1);
    Serial.println(NMEA2);
}

void clearGPS() 
{  
    while(!GPS.newNMEAreceived()) 
    {
    c=GPS.read();
    }
    GPS.parse(GPS.lastNMEA());
  
    while(!GPS.newNMEAreceived()) 
    {
        c=GPS.read();
    }
  GPS.parse(GPS.lastNMEA());

    while(!GPS.newNMEAreceived()) 
    {
        c=GPS.read();
    }
    GPS.parse(GPS.lastNMEA());
}

char generateFiles(String sensor) 
{
    //derived from code found at http://forum.arduino.cc/index.php?topic=57460.0
    String fileName = String();
    String message = String();
    unsigned int filenumber = 1;
    while(!filenumber==0) 
    {
        fileName = sensor;
        fileName += filenumber;
        fileName += ".txt";
        message = fileName;
        char charFileName[fileName.length() + 1];
        fileName.toCharArray(charFileName, sizeof(charFileName));

        if (SD.exists(charFileName)) 
        { 
            message += " exists.";
            filenumber++;
        }
        else 
        {
            File dataFile = SD.open(charFileName, FILE_WRITE);
            message += " created.";
            dataFile.close();
            filenumber = 0;
            return charFileName;
        }
    }
}
