// ==============================================================================
// DBR_controller.ino
// This Arduino program is dedicated to controlling the Down (D), Back (B), and
// Right (R) faces of a Rubik's Cube in a multi-Arduino cube solving robot.
// 
// - This controller receives move commands via serial (see BAUD_RATE).
// - It is responsible for executing only the D, B, and R face moves.
// - Each face is mapped to a stepper motor, defined by MOTOR1_FACE, MOTOR2_FACE,
//   and MOTOR3_FACE.
// - The main logic for interpreting commands and driving motors is handled by
//   the controller_funcs.h library.
// 
// NOTE: This file should be deployed to the Arduino responsible for the DBR faces.
// ==============================================================================

#include <controller_funcs.h>

// Define some macros

#define BAUD_RATE 9600
#define MOTOR1_FACE "D"
#define MOTOR2_FACE "B"
#define MOTOR3_FACE "R"
#define STEP_DELAY 1000

// Main program methods are handled by the library

void setup() {
  controllerSetup(BAUD_RATE,
                  MOTOR1_FACE,
                  MOTOR2_FACE,
                  MOTOR3_FACE,
                  STEP_DELAY);
}

void loop() {
  controllerLoop();
}
