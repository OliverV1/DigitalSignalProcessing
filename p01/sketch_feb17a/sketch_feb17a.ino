int analogPin = A0;
int val = 0; 
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600); 
}

void loop() {
  
  val = analogRead(analogPin);
  delay(50);
  Serial.println(val); 
}
