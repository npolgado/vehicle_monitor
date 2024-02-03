// IO_BOARD - Arduino code to process controls and serialize it

// RIDE HEIGHTS
#define PIN_LEFT_R_WHL          A0
#define PIN_RIGHT_R_WHL         A1

#define PIN_LEFT_F_WHL          A2
#define PIN_RIGHT_F_WHL         A3

// SWITCHES
#define SWITCH_RECORD_START     2
#define SWITCH_RECORD_STOP      3
#define SWITCH_PLAYBACK_START   4
#define SWITCH_PLAYBACK_STOP    5
#define SWITCH_LIVE             6
#define SWITCH_CALIBRATE        7

// CONSTANTS
#define STOP_BIT                3030
#define RATE                    10    // in ms

/*

EX DATA from Ride Height 

~100 (0x64)  minumum

~950 (0x3E8) maximum

*/ 

// function: serialize. Take the array of integers and serialize it to a char array


void setup() {
  // Initialize serial communication at a baud rate of 9600
  Serial.begin(9600);

  pinMode(PIN_LEFT_R_WHL, INPUT);
  pinMode(PIN_RIGHT_R_WHL, INPUT);
  pinMode(PIN_LEFT_F_WHL, INPUT);
  pinMode(PIN_RIGHT_F_WHL, INPUT);

  pinMode(SWITCH_RECORD_START, INPUT);
  pinMode(SWITCH_RECORD_STOP, INPUT);
  pinMode(SWITCH_PLAYBACK_START, INPUT);
  pinMode(SWITCH_PLAYBACK_STOP, INPUT);
  pinMode(SWITCH_LIVE, INPUT);
  pinMode(SWITCH_CALIBRATE, INPUT);
  
  while (!Serial); // Wait untilSerial is ready 
}

void loop() {
  // Read analog values from ride heights
  uint16_t analogValueA0 = analogRead(A0);
  uint16_t analogValueA1 = analogRead(A1);
  uint16_t analogValueA2 = analogRead(A2);
  uint16_t analogValueA3 = analogRead(A3);

  // Read digital values from switches
  uint16_t sw_start = digitalRead(SWITCH_RECORD_START);
  uint16_t sw_stop = digitalRead(SWITCH_RECORD_STOP);
  uint16_t sw_playback_start = digitalRead(SWITCH_PLAYBACK_START);
  uint16_t sw_playback_stop = digitalRead(SWITCH_PLAYBACK_STOP);
  uint16_t sw_live = digitalRead(SWITCH_LIVE);
  uint16_t sw_calibrate = digitalRead(SWITCH_CALIBRATE);

  // create an integer array to store the values
  uint16_t data[11] = {analogValueA0, analogValueA1, analogValueA2, analogValueA3, sw_start, sw_stop, sw_playback_start, sw_playback_stop, sw_live, sw_calibrate, STOP_BIT};
  
  
  // serialized_data[i] = data[i];
  // serialize the data
  char serialized_data[20];
  for (int i = 0; i < 10; i++) {
    // cast 16 bit inter to 8 bit char of hex
    char hex[5];
    sprintf(hex, "%04X", data[i]);
    // copy the hex to the serialized_data
    for (int j = 0; j < 4; j++) {
      serialized_data[i*4 + j] = hex[j];
    }

  }


  // Print the values over the serial port
  // Serial.println(analogValueA0); // , HEX
  // Serial.println(analogValueA1); // , HEX
  // Serial.println(analogValueA2); // , HEX
  // Serial.println(analogValueA3); // , HEX
  // Serial.println(stop_bit);

  delay(RATE);
}
