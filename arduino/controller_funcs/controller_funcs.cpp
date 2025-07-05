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

    Serial.begin(baudRate);
    Serial.println("Controller setup complete.");
    Serial.print("Motor 1 Face: ");
    Serial.println(motor1Face);
    Serial.print("Motor 2 Face: ");
    Serial.println(motor2Face);
    Serial.print("Motor 3 Face: ");
    Serial.println(motor3Face);
}

void controllerLoop() {
    while (!Serial.available());

    String cube_move = Serial.readStringUntil("E");
	cube_move.remove(cube_move.length() - 2); // Remove the end character "E"

    Serial.println("Received move: " + cube_move);
}
