// OLED Library includes
#include "U8x8lib.h" // include the fast graphics library
#include "Wire.h"    // include the I2C library

U8X8_SSD1306_128X32_UNIVISION_HW_I2C oled(U8X8_PIN_NONE);

// Clear the display no more than once per second
const int MAX_REFRESH = 1000;
unsigned long lastClear = 0;

void setupDisplay() {
  oled.begin();           // Initializes u8x8 object
  oled.setPowerSave(0);   // Makes sure OLED doesn't go to sleep
  oled.setFont(u8x8_font_amstrad_cpc_extended_r); // Set the font
  oled.setCursor(0, 0);   // Sets the cursor at the top left corner
}

void writeDisplay(const char * message, int row, bool erase) {
  unsigned long now = millis();
  // if erase is true and it's been longer than MAX_REFRESH (1s)
  if(erase && (millis() - lastClear >= MAX_REFRESH)) {
    oled.clearDisplay();
    lastClear = now;
  }
  oled.setCursor(0, row);
  oled.print(message);
}

void writeDisplayCSV(String message, int commaCount) {
  int startIndex = 0;
  for(int i=0; i<=commaCount; i++) {
    // find the index of the comma and store it in startIndex
    int index = message.indexOf(',', startIndex);

    // take everything in the string up until the comma
    String subMessage = message.substring(startIndex, index);

    startIndex = index + 1; // skip over the comma

    // Write the substring onto the OLED!
    writeDisplay(subMessage.c_str(), i, false);
  }
}
