/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int detectReading = 0;
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;

unsigned long motorTime = 0;
unsigned long yTime = 0;
unsigned long rTime = 0;
unsigned long bTime = 0;

const int BLU_LED = 12;
const int YEL_LED = 27;
const int RED_LED = 33;

int bBlinks = 0;
bool blueOn = false;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  setupButtons();
  setupMotor();

  pinMode(BLU_LED, OUTPUT);
  pinMode(YEL_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  sending = false;

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);
}

/*
 * The main processing loop
 */
void loop() {

  getButton();
  
  // Parse command coming from Python (either "stop" or "start")
  String command = receiveMessage();
  
  if(command == "stop") {
    sending = false;
    writeDisplay("Controller: Off", 0, true);
  }
  else if(command == "start") {
    sending = true;
    writeDisplay("Controller: On", 0, true);
  }
  else if(command == "buzz") {
    digitalWrite(YEL_LED, HIGH);
    yTime = millis();
    activateMotor(255);
    motorTime = millis();
  }
  else if(command.substring(0,5) == "Score") {
    String score = command.substring(6);
    String score_msg = "Your Score: " + score;
    
    writeDisplay(score_msg.c_str(), 1, true);
  }
  else if(command.substring(0,5) == "Lives") {
    writeDisplay(command.c_str(), 0, true);
  }
  //else if(command == "quit") {
  //  digitalWrite(RED_LED, HIGH);
  //  rTime = millis();
  //}
  else if(command == "pause") {
    digitalWrite(BLU_LED, HIGH);
    blueOn = true;
    bTime = millis();
  }
  else if(command.substring(0,3) == "End") {
    digitalWrite(RED_LED, HIGH);
    rTime = millis();
    writeDisplay(command.c_str(), 3, true);
  }

  detectQuit();

  // Send the orientation of the board
  
  if(sending && sampleSensors()) {
    sendMessage(String(getOrientation()));
  }

  if(millis() - motorTime >= 1000) {
    deactivateMotor();
  }

  if(millis() - yTime >= 500) {
    digitalWrite(YEL_LED, LOW);
  }
  
  if(millis() - rTime >= 1000) {
    digitalWrite(RED_LED, LOW);
  }
  
  if(millis() - bTime >= 500 && bBlinks < 5 && blueOn) {
    bTime = millis();
    bBlinks += 1;

    if(digitalRead(BLU_LED) == HIGH){
      digitalWrite(BLU_LED, LOW);
    }
    else {
      digitalWrite(BLU_LED, HIGH);
    }
  }
  else if(bBlinks > 4){
    bBlinks = 0;
    blueOn = false;
    digitalWrite(BLU_LED, LOW);
  }
  
  /*
  if(sampleSensors()){
    Serial.println(xyz());
    Serial.println(ppgPrint());
  }
  */
  
}
