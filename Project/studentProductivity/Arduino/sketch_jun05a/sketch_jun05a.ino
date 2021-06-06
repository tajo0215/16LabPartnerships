

void setup() {
  // put your setup code here, to run once:
  setupCommunication();
  setupButtons();
  setupDisplay();
  setupMotor();

  
}

void loop() {
  // put your main code here, to run repeatedly:
  String command = receiveMessage();
}
