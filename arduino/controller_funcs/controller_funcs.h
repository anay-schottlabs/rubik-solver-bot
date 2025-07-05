#ifndef CONTROLLER_FUNCS_H
#define CONTROLLER_FUNCS_H

#include <Arduino.h>

void controllerSetup(unsigned int baudRate,
                      String motor1Face,
                      String motor2Face,
                      String motor3Face);

void controllerLoop();

#endif
