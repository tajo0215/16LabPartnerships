const int btnPin = 14;

int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;

String dataStore[250][4];
bool collectData = true;
int idxr = 0;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  pinMode(btnPin, INPUT_PULLUP);
  sending = false;
  writeDisplay("Sleep", 0, true);
}


void loop() {
  int btnPress = digitalRead(btnPin);
  String command = receiveMessage();

  if (btnPress == LOW) {
    String inputStr = "";
    int i;
    for(i = 0; i < 200; i++){
      inputStr += dataStore[i][0] + "," + dataStore[i][1] + "," + dataStore[i][2] + "," + dataStore[i][3] + ",";
    }
    collectData = false;
    sendMessage(inputStr);
  }
  if (command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if (command == "wearable") {
    sending = true;
    collectData = true;
    writeDisplay("Wearable", 0, true);
  } else if (command.substring(0, 5) == "Count") {
    String jump_count = command.substring(5);
    String msg = "Jumps: " + jump_count;
    writeDisplay(msg.c_str(), 2, true);
  }
  if (sending && sampleSensors()) {
    if (collectData && idxr + 1 < 201) {
      dataStore[idxr][0] = String(sampleTime);
      dataStore[idxr][1] = String(ax);
      dataStore[idxr][2] = String(ay);
      dataStore[idxr][3] = String(az);
      idxr += 1;
    }
  }
}
