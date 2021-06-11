
const int BLU_LED = 27;
const int YEL_LED = 12;
const int RED_LED = 33;

unsigned long eventStartTime = 0;
unsigned long eventStartMotor = 0;
unsigned long pomoTimerStart = 0;
unsigned long habitTimer = 0;

unsigned long motorTime1 = 0;
unsigned long motorTime2 = 0;
unsigned long yTime = 0;
unsigned long rTime = 0;
unsigned long bTime = 0;

int rBlinks = 0;
bool redOn = false;

bool pause_timer = false;
bool start_timer = false;
bool sending = false;

void setup() {
  // put your setup code here, to run once:
  setupCommunication();
  setupButtons();
  setupDisplay();
  setupMotor();

  pinMode(BLU_LED, OUTPUT);
  pinMode(YEL_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  
  writeDisplay("Hello", 1, true);
}

void loop() {
  // put your main code here, to run repeatedly:
  String command = receiveMessage();

  if (command.substring(0, 5) == "event"){
    command = command.substring(command.indexOf(",") + 1);
    String startTime = "Start: " + command.substring(0, command.indexOf(",")); 
    command = command.substring(command.indexOf(",") + 1);
    String endTime = "End: " + command.substring(0, command.indexOf(","));
    String event = "Event: " + command.substring(command.indexOf(",") + 1);

    writeDisplay(event.c_str(), 0, false);
    writeDisplay(startTime.c_str(), 1, false);
    writeDisplay(endTime.c_str(), 2, false);

    digitalWrite(BLU_LED, HIGH);
    activateMotor(255);
    eventStartTime = millis();
    eventStartMotor = millis();
    
  } 
  else if (command == "Timer Ready"){
    sending = true;
  } 
  else if (command.substring(0, 5) == "Habit"){
    command = command.substring(5);
    String habit_name = "Habit: " + command.substring(0, command.indexOf(','));
    writeDisplay(habit_name.c_str(), 2, true);
    digitalWrite(YEL_LED, HIGH);
    habitTimer = millis();
  } 
  else if(command.substring(0,5) == "Focus"){
    String s1 = command.substring(0, command.indexOf(","));
    command = command.substring(command.indexOf(",") + 2);

    String msg1 = s1 + "!";
    String msg2 = command + "!!";

    writeDisplay(msg1.c_str(), 0, true);
    writeDisplay(msg2.c_str(), 1, true);  

    digitalWrite(YEL_LED, HIGH);
    yTime = millis();
    activateMotor(255);
    motorTime1 = millis();
  }
  else if(command.substring(0,4) == "Hang"){
    String s1 = command.substring(0, command.indexOf(","));
    command = command.substring(command.indexOf(",") + 2);

    writeDisplay(s1.c_str(), 0, true);
    writeDisplay(command.c_str(), 1, true);

    digitalWrite(RED_LED, HIGH);
    redOn = true;
    rTime = millis();
    activateMotor(255);
    motorTime2 = millis();
  }
  else if(command.substring(0,5) == "Ooops"){
    String s1 = command.substring(0, command.indexOf(","));
    command = command.substring(command.indexOf(",") + 2);
    
    writeDisplay(s1.c_str(), 0, true);
    writeDisplay(command.c_str(), 1, true);

    digitalWrite(RED_LED, HIGH);
    redOn = true;
    rTime = millis();
    activateMotor(255);
    motorTime2 = millis();
  }
  else if(command.substring(0,5) == "Chill"){
    String s1 = command.substring(0, command.indexOf(","));
    command = command.substring(command.indexOf(",") + 2);

    String msg1 = s1 + "!";

    writeDisplay(msg1.c_str(), 0, true);
    writeDisplay(command.c_str(), 1, true);

    digitalWrite(YEL_LED, HIGH);
    yTime = millis();
    activateMotor(255);
    motorTime1 = millis();
  }
  else if(command.substring(0,5) == "Good"){
    String s1 = command.substring(0, command.indexOf("!"));
    command = command.substring(command.indexOf("!") + 2);

    writeDisplay(s1.c_str(), 0, true);
    writeDisplay(command.c_str(), 1, true);

    digitalWrite(BLU_LED, HIGH);
    bTime = millis();
    activateMotor(255);
    motorTime1 = millis();
  }

  if (sending && getButton() == 1){
    if(!start_timer){
      sendMessage("start");
      start_timer = true;
    } else if(start_timer && !pause_timer){
      sendMessage("pause");
      pause_timer = true;
    } else if(start_timer && pause_timer){
      sendMessage("continue");
      pause_timer = false;
    }
  }

  if (sending && getButton() == 2){
    sendMessage("restart timer");
  }

  if(millis() - eventStartTime >= 5000){
    digitalWrite(BLU_LED, LOW);
  }
  if(millis() - eventStartMotor >= 2500){
    deactivateMotor();
  }

  if (millis() - habitTimer >= 5000 && getButton() == 3){
    digitalWrite(YEL_LED, LOW);
  }

  if(millis() - motorTime1 >= 1000) {
    deactivateMotor();
  }

  if(millis() - motorTime2 >= 2000) {
    deactivateMotor();
  }

  if(millis() - bTime >= 3000) {
    digitalWrite(BLU_LED, LOW);
  }

  if(millis() - yTime >= 3000) {
    digitalWrite(YEL_LED, LOW);
  }

  if(millis() - rTime >= 500 && rBlinks < 5 && redOn) {
    rTime = millis();
    rBlinks += 1;

    if(digitalRead(RED_LED) == HIGH){
      digitalWrite(RED_LED, LOW);
    }
    else {
      digitalWrite(RED_LED, HIGH);
    }
  } else if(rBlinks > 4){
    rBlinks = 0;
    redOn = false;
    digitalWrite(RED_LED, LOW);
  }
}
