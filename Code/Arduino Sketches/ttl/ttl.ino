
#include <Adafruit_GPS.h>
Adafruit_GPS GPS(&Serial);

String NMEA1;
String NMEA2;
char c; 

void setup() 
{
    GPS.begin(9600);
    GPS.sendCommand("$PGCMD,33,0*6D");
    GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
    GPS.sendCommand(PMTK_SET_NMEA_UPDATE_10HZ);
   // GPS.end();
}

void loop() 
{
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
