// ----------------------------------------------------------------------------------------------------
// =========== OLED Display ============ 
// ----------------------------------------------------------------------------------------------------

/* 
 * OLED Display Include and Settings
 */
#include "U8x8lib.h"                                      // include the fast graphics library
#include <Wire.h>                                         // include the Wire protocol (to communicate over I2C)

U8X8_SSD1306_128X32_UNIVISION_HW_I2C oled(U8X8_PIN_NONE); // instantiate the display object "oled"
const int MAX_REFRESH = 1000;                             // limit the screen clearing to at most once per second
unsigned long lastClear = 0;                              // the last time we updated the screen

/*
 * Initialize the OLED with a fixed base font for fast refresh.
 */
void setupDisplay() {
  oled.begin();
  oled.setPowerSave(0);
  oled.setFont(u8x8_font_amstrad_cpc_extended_r);
  oled.setCursor(0, 0);
}

/*
 * A function to write a message on the OLED display.
 * The "row" argument specifies which row to print on. Valid values are [0, 1, 2, 3].
 * The "erase" argument specifies if the display should be cleared first or not.
 */
void writeDisplay(const char *message, int row, bool erase) {
  unsigned long now = millis();
  if(erase && (millis() - lastClear >= MAX_REFRESH)) {
    oled.clearDisplay();
    lastClear = now;
  }
  oled.setCursor(0, row);
  oled.print(message);
}

/*
 * A function to write a CSV (comma-separated) message on multiple lines on the OLED.
 * The commaCount argument specifies how many commas are in the String.
 * NOTE: The OLED can only display 4 lines of text (a maximum of 3 commas).
 */
void writeDisplayCSV(String message, int commaCount) {
  int startIndex = 0;
  for(int i=0; i<=commaCount; i++) {
    int index = message.indexOf(',', startIndex);
    String subMessage = message.substring(startIndex, index);
    startIndex = index + 1;
    writeDisplay(subMessage.c_str(), i, false);
  }
}
