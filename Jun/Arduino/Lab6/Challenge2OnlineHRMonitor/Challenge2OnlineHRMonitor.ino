int ax = 0; int ay = 0; int az = 0;
int ppg = 0;
int sampleTime = 0;
bool sending;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
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

  else if (command.substring(0,2) == "HR") {
    String hr_count = command.substring(2);
    String hr = "HR: " + hr_count;
    writeDisplay(hr.c_str(), 2, true);
  }

  if (sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(ppg);
    sendMessage(response);
  }
}
