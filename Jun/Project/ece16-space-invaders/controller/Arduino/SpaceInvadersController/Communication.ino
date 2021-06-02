// ----------------------------------------------------------------------------------------------------
// =========== Communication Code for Messaging via Hardware Serial or Bluetooth ============ 
// ----------------------------------------------------------------------------------------------------

/*
 * Precompiler directive elegance: 0 == Serial, 1 == Bluetooth
 */
#define USE_BT 0

/*
 * This block allows us to use "Ser" throughout our codebase.
 * This makes the code to be protocol-agnostic.
 * Whether using Bluetooth or USB Serial, we will reference it as Ser.
 */
#if USE_BT
  #include "BluetoothSerial.h"
  BluetoothSerial SerialBT;     // instantiate a BT object
  #define Ser SerialBT          // substitute Ser for SerialBT
#else
  #define Ser Serial            // substitute Ser for Serial
#endif

/*
 * Initialize the communication protocol (either HW Serial or BT)
 */
void setupCommunication() {
  #if USE_BT
    Ser.begin("zzangu"); // any unique name for BT identification
  #else
    Ser.begin(115200);
  #endif
}

/*
 * Receive a message one character at a time, stopping at a newline ('\n')
 */
String receiveMessage() {
  String message = "";
  if (Ser.available() > 0) {
    while (true) { // loop forever until a newline is seen
      char c = Ser.read();
      if (c != char(-1)) { // if there is a character in the buffer
        if (c == '\n')
          break;
        message += c;
      }
    }
  }
  return message;
}


/*
 * Send a message over the communication protocol
 */
void sendMessage(String message) {
  Ser.println(message);
}
