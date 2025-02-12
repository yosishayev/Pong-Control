#include "mySensor.h"      // Include the sensor library
#include "myButtons.h"      // Include the button library
#include "myDistance.h"     // Include the distance measurement library

void setup() {
  // Initialize the system components
  set();                  // Set up the sensor
  setButtons();           // Set up the buttons
  setDis();               // Set up the distance sensor
  
  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);     
}

void loop() {
  // Read and print the color sensor data for the left and right outputs
  Serial.println(readColor(S12, S13, OUT1) + "L");  // Left output
  Serial.print(readColor(S22, S23, OUT2) + "R");    // Right output
  Serial.println("");  // Print a blank line for separation

  // Check if any buttons are pressed
  checkButton();
  
  // Execute movement based on sensor and button input
  movement();
  
  // Wait for 20 milliseconds before repeating the loop
  delay(20);
}
