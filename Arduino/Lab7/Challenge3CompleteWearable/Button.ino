const int btnPin = 14;

bool btnVal = false; //used for digitalRead
bool pressed = false, released = false; 

unsigned long timePressed = 0;
unsigned long timeReleased = 0;
unsigned long timeDiff = 0;

void setupButton(){
  pinMode(btnPin, INPUT_PULLUP);
}

bool HRBtn(){
  if(digitalRead(btnPin) == LOW && pressed == false){ //checks if button is pressed and that it wasnt already pressed
    timePressed = millis();
    pressed = true;
    released = false;
  }
  if(digitalRead(btnPin) == HIGH && released == false){ //checks that button was released and that button wasnt already released
    timeReleased = millis();
    pressed = false;
    released = true;
    timeDiff = timeReleased - timePressed;
  }

  if(timeDiff >= 1000){ //if the time is greater than 1 secs, then we can get the HR for 10 seconds
    timeDiff = 0;
    return true;
  }
  return false;
}
