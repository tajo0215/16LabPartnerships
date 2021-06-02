// ----------------------------------------------------------------------------------------------------
// =========== Code for Sampling the Sensors ============ 
// ----------------------------------------------------------------------------------------------------

/*
 * Sampling settings to read the sensors at 100 Hz
 */
int sampleRate = 100;                         // Frequency of reading the sensors (in Hz)
unsigned long sampleDelay = 1e6 / sampleRate; // Time between samples (in microseconds)
unsigned long timeStart = 0;                  // Start time timing variable
unsigned long timeEnd = 0;                    // End time timing variable

/*
 * A function to sample all the sensors at a specific frequency and send
 * Returns true if new samples are read, false otherwise
 */
bool sampleSensors() {
  timeEnd = micros();
  if(timeEnd - timeStart >= sampleDelay) {
    displaySampleRate(timeEnd);
    timeStart = timeEnd;

    // Read the sensors and store their outputs in global variables
    sampleTime = millis();
    readAccelSensor();     // values stored in "ax", "ay", and "az"
    readPhotoSensor();     // value stored in "ppg"
    return true;
  }

  return false;
}

/*
 * A helper function that calculates the sample rate and shows it on the display for every nSamples
 */
void displaySampleRate(unsigned long currentTime) {
  int nSamples = 100;
  static int count = 0;
  static unsigned long lastTime = 0;

  // Compute average sampling rate every nSamples
  count++;
  if(count == nSamples) {
    // compute average over nSamples and display it
    double avgRate = nSamples * 1e6 / (currentTime - lastTime);
    String message = String(avgRate) + " Hz";
    writeDisplay(message.c_str(), 3, false);

    // reset
    count = 0;
    lastTime = currentTime;
  }
}
