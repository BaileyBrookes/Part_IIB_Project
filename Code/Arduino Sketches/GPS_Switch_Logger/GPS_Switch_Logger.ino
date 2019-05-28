
#include <SD.h>
#include<SPI.h>

#include <Adafruit_GPS.h>
//  Libreria per la creazione di un seriale sulla porta 9600 via software. Sintassi: SoftwareSerial mySerial(TXpin, RXpin);
#include <SoftwareSerial.h>
SoftwareSerial mySerial(3,2);
//  Dichiarazione oggetto GPS con invio dei dati al seriale mySerial.
Adafruit_GPS GPS(&mySerial);

//  Variabili per le frasi NMEA
String NMEA1;
String NMEA2;
//  Variabili per la lettura dei caratteri nelle frasi NMEA
char c;         //  per legere i caratteri delle stringhe
float deg;      //  per leggere i gradi dalle stringhe
float degWhole; //  per leggere la parte intera dei gradi
float degDec;   //  per leggere la parte decimale dei gradi
int AnalogPin = 3;
int SwitchValue = 0;         
bool FirstPastFlag = true;
String GPSFile;

//  Dichiarazione del pin SS della scheda SD.
//  N.B. Controllare con precisione quale sia la comunicazione SS della propria scheda SD
//  Le logging shield hanno il pin SS su D10, di solito
//  int chipSelect = 4;
int chipSelect = 10;
//  Dichiarazione della variabile di tipo File, la useremo dopo per scrivere i log
File mySensorData;


void setup() 
{
  Serial.begin(9600);
  GPS.begin(9600);
  GPS.sendCommand("$PGCMD,33,0*6D");
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_10HZ);
  delay(1000); 
  
  SD.begin(chipSelect);
  pinMode(8,OUTPUT);

  readGPS();
}

void loop() 
{
  SwitchValue = analogRead(AnalogPin);     // read the input pin
  Serial.println(SwitchValue);
  if(SwitchValue > 900) //Only save data if switch on
  { 
    if(FirstPastFlag == true)
    {
      GPSFile      = generateFiles("GPS");
      FirstPastFlag = false;
    }
    digitalWrite(8,HIGH); 
    readGPS();
    mySensorData = SD.open(GPSFile, FILE_WRITE);
    mySensorData.println(NMEA1);                    
    mySensorData.println(NMEA2);                    
    mySensorData.close();
  }   
  else
  {
    digitalWrite(8,LOW);
    FirstPastFlag = true;                        
  }
}

void readGPS() {
  
  clearGPS();
  while(!GPS.newNMEAreceived()) {
    c=GPS.read();
  }

  GPS.parse(GPS.lastNMEA());
  NMEA1=GPS.lastNMEA();


   while(!GPS.newNMEAreceived()) {
    c=GPS.read();
  }
  GPS.parse(GPS.lastNMEA());
  NMEA2=GPS.lastNMEA();
 
}

void clearGPS() {  
  while(!GPS.newNMEAreceived()) {
    c=GPS.read();
  }
  GPS.parse(GPS.lastNMEA());
  
  while(!GPS.newNMEAreceived()) {
    c=GPS.read();
  }
  GPS.parse(GPS.lastNMEA());

  while(!GPS.newNMEAreceived()) {
    c=GPS.read();
  }
  GPS.parse(GPS.lastNMEA());

}
void convLong(){
  
  degWhole=float(int(GPS.longitude / 100));
  degDec=(GPS.longitude - degWhole * 100 ) / 60;
  deg = degWhole + degDec;
  if(GPS.lon=='W'){
    deg = (-1) * deg;
  }
}
void convLati(){
  degWhole=float(int(GPS.latitude / 100));
  degDec=(GPS.latitude - degWhole * 100 ) / 60;
  deg = degWhole + degDec; 
  if(GPS.lat=='S'){
    deg = (-1) * deg;
  }
}

String generateFiles(String sensor) 
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
            return fileName;
        }
    }
}
