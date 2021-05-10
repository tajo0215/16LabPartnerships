int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = false;
  writeDisplay("Sleep", 0, true);
}

void loop() {
  
  String command = receiveMessage();
  
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  } 
  else if (command.substring(0, 5) == "Walks"){
    String step_count = command.substring(5);
    String steps = "Walks: " + step_count;
    writeDisplay(steps.c_str(), 2, true);
  }
  
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
  }
}
