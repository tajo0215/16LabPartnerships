// Accelerometer Pins
const int X_PIN = A0; 
const int Y_PIN = A1;
const int Z_PIN = A2;

void setupAccelSensor(){
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(Z_PIN, INPUT);
}

void readAccelSensor(){
  ax = analogRead(X_PIN);
  ay = analogRead(Y_PIN);
  az = analogRead(Z_PIN);
  
}
