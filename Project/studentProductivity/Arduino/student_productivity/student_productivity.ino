
const int BLU_LED = 27;
const int YEL_LED = 12;
const int RED_LED = 33;

unsigned long eventStartTime = 0;
unsigned long eventStartMotor = 0;

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

  if(millis() - eventStartTime >= 5000){
    digitalWrite(BLU_LED, LOW);
  }
  if(millis() - eventStartMotor >= 2500){
    deactivateMotor();
  }
}
