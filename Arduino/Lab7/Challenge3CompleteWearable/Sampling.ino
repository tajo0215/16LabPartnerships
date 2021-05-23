int sampleRate = 50;                          // Sensor reading Frequency (Hz)
unsigned long sampleDelay = 1e6/sampleRate;   // Time(us) between samples
unsigned long timeStart = 0;                  // Start time timing variable
unsigned long timeEnd = 0;                    // End time timing variable

bool sampleSensors() {
  timeEnd = micros();

  if(timeEnd - timeStart >= sampleDelay) {
    displaySampleRate(timeEnd);
    timeStart = timeEnd;

    // Read the sensors and store their outputs in global variables
    sampleTime = millis();
    readAccelSensor();      // values stored in "ax", "ay", and "az"
    readPhotoSensor();      // values stored in "ppg"

    return true;
  }

  return false;
}

void displaySampleRate(unsigned long currentTime) {
  int nSamples = 100;
  static int count = 0;
  static unsigned long lastTime = 0;

  count++;

  if(count == nSamples) {
    double avgRate = nSamples * 1e6 / (currentTime - lastTime);
    String message = String(avgRate) + "Hz";
    writeDisplay(message.c_str(), 4, false);

    // reset
    count = 0;
    lastTime = currentTime;
  }
}
