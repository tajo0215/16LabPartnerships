/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;

const int rBtn = 32;
const int lBtn = 14;
const int pauseBtn = 15;
const int rLED = 33;
const int bLED = 27;
const int yLED = 12;

bool prevStateL = LOW;
bool prevStateR = LOW;
bool prevStatePause = LOW;
bool blueOn = false;

unsigned long motorTime = 0;
unsigned long rTime = 0;
unsigned long bTime = 0;

int bBlinks = 0;
/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  setupMotor();

  pinMode(rBtn, INPUT_PULLUP);
  pinMode(lBtn, INPUT_PULLUP);
  pinMode(pauseBtn, INPUT_PULLUP);
  pinMode(rLED, OUTPUT);
  pinMode(bLED, OUTPUT);
  pinMode(yLED, OUTPUT);
  
  sending = false;

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);
}

/*
 * The main processing loop
 */
void loop() {

  int lb = digitalRead(lBtn);
  int rb = digitalRead(rBtn);
  int pb = digitalRead(pauseBtn);

  if(lb == LOW && prevStateL == HIGH && sending){
    sendMessage("9");
  }
  prevStateL = lb;

  if(rb == LOW && prevStateR == HIGH && sending){
    sendMessage("10");
  } 
  prevStateR = rb;

  if(pb == LOW && prevStatePause == HIGH && sending){
    sendMessage("11");
  }
  prevStatePause = pb;
  
  // Parse command coming from Python (either "stop" or "start")
  String command = receiveMessage();
  if(command == "stop") {
    sending = false;
    String msg = "Controller: Off";
    writeDisplay(msg.c_str(), 0, true);
  }
  else if(command == "start") {
    sending = true;
    String msg = "Controller: On";
    writeDisplay(msg.c_str(), 0, true);
  } else if(command == "buzz"){
    digitalWrite(yLED, HIGH);
    activateMotor(255);
    motorTime = millis();
  } else if(command.substring(0, 5) == "Score"){
    String score = command.substring(7);
    String score_msg = "Score: " + score;
    writeDisplay(score_msg.c_str(), 2, true);
  } else if(command == "quit"){
    digitalWrite(rLED, HIGH);
    rTime = millis();
  } else if(command == "pause"){
    digitalWrite(bLED, HIGH);
    blueOn = true;
    bTime = millis();
  }

  // Send the orientation of the board
  if(sending && sampleSensors()) {
    sendMessage(String(getOrientation()));
  }

  if(millis() - motorTime >= 1000){
    deactivateMotor();
    digitalWrite(yLED, LOW);
  }
  if(millis() - rTime >= 1000){
    digitalWrite(rLED, LOW);
  }
  if(millis() - bTime >= 500 && bBlinks < 5 && blueOn){
    bTime = millis();
    bBlinks += 1;
    if (digitalRead(bLED) == HIGH){
      digitalWrite(bLED, LOW);
    } else {
      digitalWrite(bLED, HIGH);
    }
  } else if(bBlinks > 4){
    bBlinks = 0;
    blueOn = false; 
    digitalWrite(bLED, LOW);
  }
}
