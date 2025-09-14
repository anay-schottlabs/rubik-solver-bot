#include "controller_funcs.h"

// Variables that will be used in the controller functions
unsigned int baudRate;
String motor1Face;
String motor2Face;
String motor3Face;
unsigned int stepDelay;

// Pin definitions for stepper motors
const int StepX = 2;
const int DirX = 5;
const int StepY = 3;
const int DirY = 6;
const int StepZ = 4;
const int DirZ = 7;

// Pin definitions for reed switches
const int ReedX = 9;
const int ReedY = 10;
const int ReedZ = 11;

// Variable to prevent moves to be executed multiple times
String lastMove;

void step(int stepPin, int stepDelay) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelay);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelay);
}

void controllerSetup(unsigned int baudRate, String motor1Face, String motor2Face, String motor3Face, unsigned int stepDelay) {
    ::baudRate = baudRate;
    ::motor1Face = motor1Face;
    ::motor2Face = motor2Face;
    ::motor3Face = motor3Face;
    ::stepDelay = stepDelay;

    Serial.begin(baudRate); // Initialize serial communication at the specified baud rate

    // Initialize stepper motor pins
    pinMode(StepX,OUTPUT);
    pinMode(DirX,OUTPUT);
    pinMode(StepY,OUTPUT);
    pinMode(DirY,OUTPUT);
    pinMode(StepZ,OUTPUT);
    pinMode(DirZ,OUTPUT);

    // Initialize reed switch pins
    pinMode(ReedX, INPUT_PULLUP); // Use pull-up resistor for reed switch
    pinMode(ReedY, INPUT_PULLUP); // Use pull-up resistor for reed switch
    pinMode(ReedZ, INPUT_PULLUP); // Use pull-up resistor for reed switch

    pinMode(LED_BUILTIN, OUTPUT); // Initialize the built-in LED pin
    digitalWrite(LED_BUILTIN, LOW); // Turn off the LED initially
}

void controllerLoop() {
    if (Serial.available()) {
        String cube_move = Serial.readStringUntil("\n");
        cube_move.trim(); // Remove any leading or trailing whitespace

        if (cube_move == lastMove) {
            return;
        }

        lastMove = cube_move; // Store the last move

    	// Check if this arduino is the one that should perform the move
    	if (cube_move.startsWith(motor1Face)
        	|| cube_move.startsWith(motor2Face)
        	|| cube_move.startsWith(motor3Face)) {
            
            	digitalWrite(LED_BUILTIN, HIGH); // Turn on the LED

            	// ----- Perform the move (stepper motor control) -----

                // set direction, HIGH for clockwise, LOW for counterclockwise
                bool isClockwise = !cube_move.endsWith("'"); // prime notation (') indicates counterclockwise
                digitalWrite(DirX, isClockwise ? HIGH : LOW);
                digitalWrite(DirY, isClockwise ? HIGH : LOW);
                digitalWrite(DirZ, isClockwise ? HIGH : LOW);

                // determine the number of steps
                int times = cube_move.indexOf("2") == -1 ? 1 : 2; // 2x the amount of steps for moves like F2

                // determine which motor to move based on the face in the move string
                // also find the corresponding reed switch pin for homing
                int stepPin;
                int reedPin;

                if (cube_move.startsWith(motor1Face)) {
                    stepPin = StepX;
                    reedPin = ReedX;
                } else if (cube_move.startsWith(motor2Face)) {
                    stepPin = StepY;
                    reedPin = ReedY;
                } else if (cube_move.startsWith(motor3Face)) {
                    stepPin = StepZ;
                    reedPin = ReedZ;
                }
                
                // If it is a double movement (e.g. F2) repeat the whole thing twice
                for (int i = 0; i < times; i++) {
                    // the motor will start in a 90 degree position, so the reed switch will be triggered by default
                    // rotate until the reed switch is no longer triggered, so that we can wait until the next 90 degree trigger
                    while (digitalRead(reedPin) == LOW) {
                        step(stepPin, stepDelay);
                    }

                    // keep moving until the reed switch is triggered again
                    // once the reed switch is triggered again, the motor has reached 90 degrees (roughly)
                    while (digitalRead(reedPin) == HIGH) {
                        step(stepPin, stepDelay);
                    }
                }

            	// Echo back the received move, this lets the python script know that everything was processed correctly
            	Serial.println(cube_move);
    	}
        else
        {
            // If the move is not for this arduino, turn off the LED
            digitalWrite(LED_BUILTIN, LOW);
        }
    }
}
