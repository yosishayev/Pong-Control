#ifndef MYBUTTONS_H
#define MYBUTTONS_H

#include <Arduino.h>

// External flags to indicate button states
extern int flag2;
extern int flag3;
extern int flag4;

// Analog pins connected to the buttons
const int analogPin1 = A0;
const int analogPin2 = A1;
const int analogPin3 = A2;

// Function declarations
void setButtons();    // Function to initialize button settings
void checkButton();   // Function to check button states

#endif
