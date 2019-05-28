#include <SD.h>
String data;
File GPST;

void setup() {
    Serial.begin(9600);
    Serial.write("$PMTK314,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29<CR><LF>");
    Serial.println("GGA sentences seleceted");
    Serial.write("$PMTK220,200*2C<CR><LF>");
    Serial.println("5Hz seleceted");
    SD.begin(10);

}

void loop() {
    //Serial.println("Before read string until");
    data = Serial.readStringUntil('$');
    //Serial.println("After read string until");
    Serial.println(data);
    GPST = SD.open("GPST.txt", FILE_WRITE);
    GPST.println(data);
    GPST.close();
}
