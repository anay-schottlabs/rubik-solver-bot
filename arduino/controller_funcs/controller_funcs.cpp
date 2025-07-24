#include "controller_funcs.h"

// Variables that will be used in the controller functions
unsigned int baudRate;
String motor1Face;
String motor2Face;
String motor3Face;
unsigned int stepDelay;
const int StepX = 2;
const int DirX = 5;
const int StepY = 3;
const int DirY = 6;
const int StepZ = 4;
const int DirZ = 7;

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

    pinMode(LED_BUILTIN, OUTPUT); // Initialize the built-in LED pin
    digitalWrite(LED_BUILTIN, LOW); // Turn off the LED initially
}

void controllerLoop() {
    if (Serial.available()) {
        String cube_move = Serial.readString();

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
                int steps = cube_move.indexOf("2") == -1 ? 50 : 100; // 2x the amount of steps for moves like F2

                // determine which motor to move based on the face in the move string
                int stepPin;
                if (cube_move.startsWith(motor1Face)) {
                    stepPin = StepX;
                } else if (cube_move.startsWith(motor2Face)) {
                    stepPin = StepY;
                } else if (cube_move.startsWith(motor3Face)) {
                    stepPin = StepZ;
                }

                // do the steps to move the motor
                for (int i = 0; i < steps; i++) {
                    digitalWrite(stepPin,HIGH);
                    delayMicroseconds(stepDelay);
                    digitalWrite(stepPin,LOW); 
                    delayMicroseconds(stepDelay);
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
