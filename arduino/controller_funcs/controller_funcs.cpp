#include "controller_funcs.h"

// Variables that will be used in the controller functions
unsigned int baudRate;
String motor1Face;
String motor2Face;
String motor3Face;

void controllerSetup(unsigned int baudRate, String motor1Face, String motor2Face, String motor3Face) {
    ::baudRate = baudRate;
    ::motor1Face = motor1Face;
    ::motor2Face = motor2Face;
    ::motor3Face = motor3Face;

    Serial.begin(baudRate); // Initialize serial communication at the specified baud rate

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

            	// Perform the move (ADD STEPPER MOTOR CODE HERE)

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
