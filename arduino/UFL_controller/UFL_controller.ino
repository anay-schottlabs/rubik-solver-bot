#include <controller_funcs.h>

// Define some macros

#define BAUD_RATE 115200
#define MOTOR1_FACE "U"
#define MOTOR2_FACE "F"
#define MOTOR3_FACE "L"

// Main program methods are handled by the library

void setup() {
  controllerSetup(BAUD_RATE,
                  MOTOR1_FACE,
                  MOTOR2_FACE,
                  MOTOR3_FACE);
}

void loop() {
  controllerLoop();
}
