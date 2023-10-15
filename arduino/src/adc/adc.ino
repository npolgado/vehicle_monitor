/*

Values from Ride Height 

~100 (0x64)  minumum

~950 (0x3E8) maximum

*/ 

// TODO: read these over I2C
int stop_bit = 0xABC;
int rate = 10; // in ms

void setup() {
  // Initialize serial communication at a baud rate of 9600
  Serial.begin(9600);
}

void loop() {
  // Read analog values from pins A0 to A3
  int analogValueA0 = analogRead(A0);
  int analogValueA1 = analogRead(A1);
  int analogValueA2 = analogRead(A2);
  int analogValueA3 = analogRead(A3);

  // Print the values over the serial port
  Serial.println(analogValueA0);
  Serial.println(analogValueA1);
  Serial.println(analogValueA2);
  Serial.println(analogValueA3);
  Serial.println(stop_bit);

  // Delay for a short period (you can adjust this value)
  delay(rate);
}
