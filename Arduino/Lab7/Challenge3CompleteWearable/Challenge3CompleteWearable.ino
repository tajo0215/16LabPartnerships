int ax = 0; int ay = 0; int az = 0;
int ppg = 0;
int sampleTime = 0;
bool sending;

const int btnPin = 14;

bool getHR = false;
unsigned long lastHR = 0;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  setupMotor();
  pinMode(btnPin, INPUT_PULLUP);
  sending = false;
  writeDisplay("Sleep", 0, true);
}

void loop() {
  String command = receiveMessage();

  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  } else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  } else if (command.substring(0,2) == "D:") {
    String weather_time = command.substring(2, command.indexOf(";"));
    command = command.substring(command.indexOf(";") + 1);
    String hr_msg = command.substring(0, command.indexOf(";"));
    String steps = command.substring(command.indexOf(";") + 1);

    writeDisplayCSV(weather_time, 2);

    if (hr_msg != "NULL"){
      String msg = "HR: " + hr_msg;
      writeDisplay(msg.c_str(), 3, false);
    } else {
      String msg = "Steps: " + steps;
      writeDisplay(msg.c_str(), 3, false);
    }
  }

  
  if (digitalRead(btnPin) == LOW){
    getHR = true;
    lastHR = millis();
  }

  
  if (sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(ppg);
    if (getHR){
      response += ",HR\n";
    } else {
      response += ",NULL\n";
    }
    sendMessage(response);
  }

  if(millis() - lastHR >= 10000){
    getHR = false;
  }
}
