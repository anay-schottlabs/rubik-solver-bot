// ==============================================================================
// UFL_controller.ino
// This Arduino program is dedicated to controlling the Up (U), Front (F), and
// Left (L) faces of a Rubik's Cube in a multi-Arduino cube solving robot.
// 
// - This controller receives move commands via serial (see BAUD_RATE).
// - It is responsible for executing only the U, F, and L face moves.
// - Each face is mapped to a stepper motor, defined by MOTOR1_FACE, MOTOR2_FACE,
//   and MOTOR3_FACE.
// - The main logic for interpreting commands and driving motors is handled by
//   the controller_funcs.h library.
// 
// NOTE: This file should be deployed to the Arduino responsible for the UFL faces.
// ==============================================================================

#include <controller_funcs.h>

// Define some macros

#define BAUD_RATE 9600
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
