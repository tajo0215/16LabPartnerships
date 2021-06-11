const int lBtn = 14;
const int cBtn = 32;
const int rBtn = 15;

bool prevStateL = LOW;
bool prevStateC = LOW;
bool prevStateR = LOW;

float pressing = 0;

int shortpress = 100;
int longpress = 2000;

void setupButtons() {
  pinMode(lBtn, INPUT_PULLUP);
  pinMode(cBtn, INPUT_PULLUP);
  pinMode(rBtn, INPUT_PULLUP);
}

int getButton() {

  int value = 0;
  
  int lb = digitalRead(lBtn);
  int cb = digitalRead(cBtn);
  int rb = digitalRead(rBtn);

  if(lb == LOW && prevStateL == HIGH) {
    value = 1;
  } else if(cb == LOW && prevStateC == HIGH) {
    value = 2;
  } else if (rb == LOW && prevStateR == HIGH){
    value = 3;
  }
  prevStateR = rb;
  prevStateC = cb;
  prevStateL = lb;

  return value;
}
