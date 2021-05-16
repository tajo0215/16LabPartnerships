#include "U8x8lib.h" // library for fast graphics
#include "Wire.h" // library for I2C

//Instantiates OLED object
U8X8_SSD1306_128X32_UNIVISION_HW_I2C oled(U8X8_PIN_NONE);

//sets refresh rate to fps
const int MAX_REFRESH = 500;
unsigned long lastClear = 0;

void setupDisplay() {
  oled.begin();
  oled.setPowerSave(0);
  oled.setFont(u8x8_font_amstrad_cpc_extended_r);
  oled.setCursor(0, 0);
}

void writeDisplay(const char * message, int row, bool erase){
  unsigned long now = millis();
  if(erase && (millis() - lastClear >= MAX_REFRESH)){
    oled.clearDisplay();
    lastClear = now;
  }
  oled.setCursor(0, row);
  oled.print(message);
}

void writeDisplayCSV(String message, int commaCount){
  int startIndex = 0;
  for(int i = 0; i <= commaCount; i++){
    int index = message.indexOf(',', startIndex);
    String subMessage = message.substring(startIndex, index);
    startIndex = index + 1;
    writeDisplay(subMessage.c_str(), i, false);
  }
}
