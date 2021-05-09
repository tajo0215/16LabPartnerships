int sampleTime = 0;
int ax = 0; int ay = 0; int az = 0;
bool sending;

const int buttonPin = 14;

const int max_samples = 500;
String jumpingjack[max_samples];
int idx = 0;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  pinMode(buttonPin, INPUT_PULLUP);
  sending = false;
  writeDisplay("Sleep", 0, true);
}

void loop() {

  int buttonPress = digitalRead(buttonPin);
  String command = receiveMessage();
  
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  
  else if(command.substring(0,5) == "Jumps"){
    String jump_count = command.substring(5);
    String jump = "Jumps: " + jump_count;
    writeDisplay(jump.c_str(), 2, true);
  }
  
  if(sending && sampleSensors()) {
    if (idx+1 <= max_samples) {
      jumpingjack[idx] = String(sampleTime) + "," + String(ax) + "," + String(ay) + "," + String(az);
      
      idx += 1;

      if (buttonPress == LOW) {
        for (int i=0; i<idx; i++) {
          sendMessage(jumpingjack[i]);
        }
      }
    }   
  }
  
}
