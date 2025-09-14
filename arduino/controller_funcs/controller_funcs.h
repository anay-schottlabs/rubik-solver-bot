#ifndef CONTROLLER_FUNCS_H
#define CONTROLLER_FUNCS_H

#include <Arduino.h>

void step(int stepPin, int stepDelay);

void controllerSetup(unsigned int baudRate,
                     String motor1Face,
                     String motor2Face,
                     String motor3Face,
                     unsigned int stepDelay);

void controllerLoop();

#endif
