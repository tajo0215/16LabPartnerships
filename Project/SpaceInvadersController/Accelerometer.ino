// ----------------------------------------------------------------------------------------------------
// =========== Accelerometer Sensor ============
// ----------------------------------------------------------------------------------------------------/*
/* Configure the analog input pins to the accelerometer's 3 axes
 */
const int X_PIN = A0;
const int Y_PIN = A1;
const int Z_PIN = A2;/*
 * Set the "zero" states when each axis is neutral
 * NOTE: Customize this for your accelerometer sensor!
 */
const int X_ZERO = 1850;
const int Y_ZERO = 1850;
const int Z_ZERO = 1950;/*
 * Configure the analog pins to be treated as inputs by the MCU
 */
void setupAccelSensor() {
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(Z_PIN, INPUT);
}/*
 * Read a sample from the accelerometer's 3 axes
 */
void readAccelSensor() {
  ax = analogRead(X_PIN);
  ay = analogRead(Y_PIN);
  az = analogRead(Z_PIN);
}String xyz() {  int x = ax - X_ZERO;
  int y = ay - Y_ZERO;
  int z = az - Z_ZERO;  int x_det = x - 70;
  int y_det = y - 70;
  int z_det = z - 420;  return String(x) + "," + String(y) + "," + String(z) + "\n" + String(x_det) + "," + String(y_det) + "," + String(z_det) + "\n";
}/*
 * Get the orientation of the accelerometer
 * Returns orientation as an integer:
 * 0 == flat
 * 1 == up
 * 2 == down
 * 3 == left
 * 4 == right
 */
int getOrientation() {
  int orientation = 0;  //  Moving Left or Right:
  //  - Left: x = |1650-1920| = 270
  //  - Right: x = 2150-1920 = 230  //  Tilting Up or Down:
  //  - Up: ay = 1600, az = 2190
  //    => y = |1600-1920| = 320, z = |2190-2380| = 190
  //  - Down: ay = 2200, az = 2150
  //    => y = |2200-1920| = 280, z = |2150-2380| = 230  // Subtract out the zeros
  int x = ax - X_ZERO;
  int y = ay - Y_ZERO;
  int z = az - Z_ZERO;  int x_det = abs(x) - 70;
  int y_det = abs(y) - 70;
  int z_det = abs(z) - 420;  // If ax has biggest magnitude, it's either left or right//  if(abs(x) >= abs(y) && abs(x) >= abs(z)) {
  if( abs(x_det) >= abs(y_det) && abs(x_det) >= abs(z_det) ) {    if( x < 70 ) {         // left
      if ( x > 0 )
        orientation = 3;
      else if( x > -70 && x <= 0)
        orientation = 4;
      else
        orientation = 5;
    }    else {                // right
      if ( x < 150 )
        orientation = 6;
      else if( x >= 150 && x < 200 )
        orientation = 7;
      else
        orientation = 8;
    }  }  // If ay has biggest magnitude, it's either up or down
  else if(abs(y_det) >= abs(x_det) && abs(y_det) >= abs(z_det)) {
    //if( y < 70 ) // up
      if( y < -150 )
        orientation = 1;
    //else        // down
      if( y > 300 )
        orientation = 2;
  }  // If az biggest magnitude, it's flat (or upside-down)
  else if(abs(z_det) > abs(x_det) && abs(z_det) >= abs(y_det)) {
    orientation = 0; // flat
  }  return orientation;
}
