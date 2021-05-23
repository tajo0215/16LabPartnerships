int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupMotor();
  sending = false;
  writeDisplay("Sleep", 0, true);
}

void loop() {
  String command = receiveMessage();
  if(command == "Sleep Mode") {
    sending = false;
    writeDisplay("Sleep Mode", 0, true);
  }
  else if(command == "Sending Data") {
    sending = true;
    writeDisplay("Sending Data", 0, true);
  } else if(command == "Idle State"){
    writeDisplay("Idle State", 0, true);
    activateMotor(255);
    delay(1000);
    deactivateMotor();
  } else if(command == "Active State"){
    writeDisplay("Stay Active!", 0, true);
  }
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
  }
}
