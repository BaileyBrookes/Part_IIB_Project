String data;

void setup() 
{
    Serial.begin(9600);
    Serial.write("$PMTK251,115200*1F<CR><LF>");
    Serial.println("Baud rate 115200 selected"); 
    Serial.write("$PMTK314,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29<CR><LF>");
    Serial.println("GGA sentences seleceted");
    Serial.write("$PMTK220,200*2C<CR><LF>");
    Serial.println("5Hz seleceted");
}

void loop()
{
    data = Serial.readStringUntil('$');
    Serial.println(data);
}
