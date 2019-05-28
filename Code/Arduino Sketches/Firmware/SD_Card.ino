
String generateFile(String sensor) 
{
    //derived from code found at http://forum.arduino.cc/index.php?topic=57460.0
    String fileName = String();
    unsigned int filenumber = 1;
    while(!filenumber==0) 
    {
        fileName = sensor;
        fileName += filenumber;
        fileName += ".txt";
        char charFileName[fileName.length() + 1];
        fileName.toCharArray(charFileName, sizeof(charFileName));

        if (SD.exists(charFileName)) 
        { 
            filenumber++;
        }
        else 
        {
            File dataFile = SD.open(charFileName, FILE_WRITE);
            dataFile.close();
            filenumber = 0;
            return fileName;
        }
    }
}
