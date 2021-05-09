const int btnPin = 14;

int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;

String dataStore[200];
bool collectData = true;
int idx = 0;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  pinMode(btnPin, INPUT_PULLUP);
  sending = false;
  writeDisplay("Sleep", 0, true);
}

bool addData() {
  if (idx + 1 <= 200) {
    dataStore[idx] = String(sampleTime) + "," + String(ax) + "," + String(ay) + "," + String(az);
    idx += 1;
    return true;
  }
  return false;
}

void loop() {
  int btnPress = digitalRead(btnPin);
  String command = receiveMessage();

  if (btnPress == LOW) {
    sendMessage("s");
      for (int i = 0; i < 200; i++) {
        sendMessage(dataStore[i]);
        dataStore[i] = "";
      }
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
    addData();
  }
}
