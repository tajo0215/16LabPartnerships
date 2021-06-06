const int lBtn = 14;
const int rBtn = 32;

bool prevStateL = LOW;
bool prevStateR = LOW;

float pressing = 0;

int shortpress = 100;
int longpress = 2000;

void setupButtons() {
  pinMode(lBtn, INPUT_PULLUP);
  pinMode(rBtn, INPUT_PULLUP);
}

void getButton() {
  
  int lb = digitalRead(lBtn);
  int rb = digitalRead(rBtn);

  if(lb == LOW && prevStateL == HIGH) {
    pressing = .01;
  }
  prevStateL = lb;
  
  if(rb == LOW && prevStateR == HIGH) {
    pressing = .01;
  }
  prevStateR = rb;
  
}
