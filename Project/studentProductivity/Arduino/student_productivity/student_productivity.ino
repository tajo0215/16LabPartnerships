// led pins 
const int BLU_LED = 27;
const int YEL_LED = 12;
const int RED_LED = 33;

// timing variables for motor and LEDs
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

  // checks for calender event 
  if (command.substring(0, 5) == "event"){
    command = command.substring(command.indexOf(",") + 1); // takes out the event string 
    String startTime = "Start: " + command.substring(0, command.indexOf(",")); // gets the start time 
    command = command.substring(command.indexOf(",") + 1);
    String endTime = "End: " + command.substring(0, command.indexOf(",")); // gets the end time 
    String event = "Event: " + command.substring(command.indexOf(",") + 1); // full event string 

    writeDisplay(event.c_str(), 0, false); // event name 
    writeDisplay(startTime.c_str(), 1, false); // start time
    writeDisplay(endTime.c_str(), 2, false); // end time 

    digitalWrite(BLU_LED, HIGH); // blue led on 
    activateMotor(255); // motor on 
    eventStartTime = millis();
    eventStartMotor = millis();
    
  } // if timer is ready, send data 
  else if (command == "Timer Ready"){
    sending = true;
  } // checks for habit 
  else if (command.substring(0, 5) == "Habit"){
    command = command.substring(5);
    String habit_name = "Habit: " + command.substring(0, command.indexOf(',')); // gets habit name 
    writeDisplay(habit_name.c_str(), 2, true); //dispalys name 
    digitalWrite(YEL_LED, HIGH); // yellow led on 
    habitTimer = millis();
  } // timer on - displays the amount of time left and Focus 
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
  } // timer on - rights hang when timer is close to being done 
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
  } // break on - writes ooops when break has 1 min left 
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
  } // chill when break is almost over 
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
  } // good when break is over and timer is over 
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

  // if timer is ready and we press button, send start 
  if (sending && getButton() == 1){
    if(!start_timer){
      sendMessage("start");
      start_timer = true;
  }

  // All the following are just timing loops to shut off functions 
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
