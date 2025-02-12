#include "mySensor.h"

// Function to read the color from the sensor
String readColor(int S2, int S3, int OUT) {
  int red, green, blue;
  float ratio1, ratio2, ratio3;

  // Read Red color
  digitalWrite(S2, LOW);
  digitalWrite(S3, LOW);
  delay(20);
  red = pulseIn(OUT, LOW, 100000);

  // Read Green color
  digitalWrite(S2, HIGH);
  digitalWrite(S3, HIGH);
  delay(20);
  green = pulseIn(OUT, LOW, 100000);

  // Read Blue color
  digitalWrite(S2, LOW);
  digitalWrite(S3, HIGH);
  delay(20);
  blue = pulseIn(OUT, LOW, 100000);

  // Calculate the ratios for color comparison
  ratio1 = (float)red / blue;
  ratio2 = (float)red / green;
  ratio3 = (float)green / blue;

  // Determine the dominant color based on the ratios
  if (ratio3 < 1.5 && ratio2 < 0.6 && 1.05 < ratio3 && 0.7 > ratio1) {
    return "CR";  // Color is Red
  } else if (ratio2 > ratio1 && ratio2 > ratio3 && ratio3 < 1.05 && ratio1 < 1.5) {
    return "CG";  // Color is Green
  } else if (ratio3 > 1.3 && ratio2 < ratio3 && ratio1 > ratio2 && ratio2 > 0.7) {
    return "CB";  // Color is Blue
  } else {
    return "CN";  // No significant color detected
  }
}

// Function to set up the sensor pins
void set() {
  // Set frequency scaling pins
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  digitalWrite(S0, HIGH);  // Set 100% frequency scaling
  digitalWrite(S1, LOW);

  // Set sensor pins
  pinMode(S10, OUTPUT);
  pinMode(S11, OUTPUT);
  pinMode(S12, OUTPUT);
  pinMode(S13, OUTPUT);
  pinMode(OUT1, INPUT);
  pinMode(S20, OUTPUT);
  pinMode(S21, OUTPUT);
  pinMode(S22, OUTPUT);
  pinMode(S23, OUTPUT);
  pinMode(OUT2, INPUT);

  // Set initial states for the sensor pins
  digitalWrite(S10, HIGH);
  digitalWrite(S11, HIGH);
  digitalWrite(S20, HIGH);
  digitalWrite(S21, HIGH);
}
