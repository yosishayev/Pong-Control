#include "myButtons.h"

// Initialize flags to track button states
int flag2 = 0;
int flag3 = 0;
int flag4 = 0;

// Function to set up button pins
void setButtons() {
  pinMode(analogPin1, INPUT_PULLUP);  // Set pin for button 1 (with internal pull-up)
  pinMode(analogPin2, INPUT_PULLUP);  // Set pin for button 2 (with internal pull-up)
  pinMode(analogPin3, INPUT_PULLUP);  // Set pin for button 3 (with internal pull-up)
}

// Function to check button states
void checkButton() {
  // Read the analog states of the buttons
  int buttonState4 = analogRead(analogPin1);
  int buttonState3 = analogRead(analogPin2);
  int buttonState2 = analogRead(analogPin3);

  // Check if button 2 is pressed (threshold value is set to 850)
  if (buttonState2 > 850 && !flag2) {  
    Serial.println("R");  // Print "R" when button 2 is pressed
    flag2 = 1;  // Set flag to indicate button press
  } else if (buttonState2 < 850) {
    flag2 = 0;  // Reset flag when button is released
  }

  // Check if button 3 is pressed
  if (buttonState3 > 850 && !flag3) {  
    Serial.println("L");  // Print "L" when button 3 is pressed
    flag3 = 1;  // Set flag to indicate button press
  } else if (buttonState3 < 850) {
    flag3 = 0;  // Reset flag when button is released
  }

  // Check if button 4 is pressed
  if (buttonState4 > 850 && !flag4) {  
    Serial.println("P" + String(buttonState4));  // Print the value of the button
    flag4 = 1;  // Set flag to indicate button press
  } else if (buttonState4 < 850) {
    flag4 = 0;  // Reset flag when button is released
  }
}
