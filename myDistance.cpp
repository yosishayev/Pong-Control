#include "myDistance.h"

// Function to set up the distance sensor pins
void setDis() {
  pinMode(trigPin, OUTPUT);  // Set Trig pin of first sensor as output
  pinMode(echoPin, INPUT);   // Set Echo pin of first sensor as input
  pinMode(trigPin2, OUTPUT); // Set Trig pin of second sensor as output
  pinMode(echoPin2, INPUT);  // Set Echo pin of second sensor as input
}

// Function to control movement based on distance readings
void movement() {
  Serial.print("l");  // Print "l" for left sensor
  Serial.println(move_pong(trigPin, echoPin));  // Get distance from left sensor
  
  Serial.print("r");  // Print "r" for right sensor
  Serial.println(move_pong(trigPin2, echoPin2));  // Get distance from right sensor
}

// Function to measure distance using an ultrasonic sensor
int move_pong(int t, int e) {
  long duration, distance;

  // Trigger the sensor to send out a pulse
  digitalWrite(t, LOW);
  delayMicroseconds(2);
  digitalWrite(t, HIGH);
  delayMicroseconds(10);
  digitalWrite(t, LOW);

  // Read the pulse duration from the Echo pin
  duration = pulseIn(e, HIGH);

  // Calculate distance in cm
  distance = duration * 0.034 / 2;  // Speed of sound is 0.034 cm/μs, divide by 2 for round-trip distance

  // Set constraints for distance
  if (distance > 30) {
    distance = 9999;  // If the distance is greater than 30 cm, set it to 9999 (out of range)
  } else if (distance > 20) {
    distance = 20;  // If the distance is between 20 and 30 cm, set it to 20 (a threshold)
  }

  // Map the distance from 0-20 cm to 0-40
  distance = map(distance, 0, 20, 0, 40);

  return distance;  // Return the final mapped distance
}
