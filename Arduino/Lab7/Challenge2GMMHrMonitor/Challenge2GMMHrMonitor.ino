int ppg = 0;
int sampleTime = 0;
bool sending;

void setup() {
  // put your setup code here, to run once:
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  writeDisplay("Sleep", 0, true);
}

void loop() {
  // put your main code here, to run repeatedly:
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
    writeDisplay(hr.c_str(), 1, true);
  }

  if (sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ppg) + "\n";
    sendMessage(response);
  }
}
