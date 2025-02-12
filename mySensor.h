#ifndef MYSENSOR_H
#define MYSENSOR_H

#include <Arduino.h>

// Define sensor pins
const int S10 = 4;
const int S11 = 5;
const int S12 = 6;
const int S13 = 7;
const int OUT1 = 8;
const int S20 = 9;
const int S21 = 10;
const int S22 = 11;
const int S23 = 12;
const int OUT2 = 13;

const int S0 = 2;
const int S1 = 3;

// Function declarations
String readColor(int S2, int S3, int OUT);
void set();

#endif
