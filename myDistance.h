#ifndef MYDISTANCE_H
#define MYDISTANCE_H

#include <Arduino.h>

// Define pin assignments for distance sensors
const int trigPin = 1;    // Trigger pin for first sensor
const int trigPin2 = 3;   // Trigger pin for second sensor
const int echoPin = 0;    // Echo pin for first sensor
const int echoPin2 = 2;   // Echo pin for second sensor

// Function declarations
void setDis();            // Function to set up the distance sensors
void movement();          // Function to control movement based on distance readings
int move_pong(int t, int e);  // Function to calculate movement based on sensor readings

#endif
