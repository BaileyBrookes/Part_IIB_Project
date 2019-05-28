int SwitchValue;
int RecSwitch = 7;

void setup() 
{
  Serial.begin(9600);
  
}

void loop() 
{
  SwitchValue = analogRead(RecSwitch);
  Serial.println(SwitchValue);

}
