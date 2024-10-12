#include <SPI.h>
#include <SD.h>
#include <NMEAGPS.h>
#include <GPSport.h>
#include <FastLED.h>

// SD card chip select pin for MKR Zero
const int chipSelect = SDCARD_SS_PIN;
const int startButton = 2;  // Start logging button on pin 2
const int stopButton = 3;   // Stop logging button on pin 3
bool isLogging = false;
File dataFile;
int fileCounter = 0;
String filename;

NMEAGPS gps;
gps_fix fix;
bool gpsValid = false;

#define NUM_LEDS 5
#define DATA_PIN 3
#define CLOCK_PIN 13
CRGB leds[NUM_LEDS];

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  
  // Setup buttons with internal pullup resistors
  pinMode(startButton, INPUT_PULLUP);
  pinMode(stopButton, INPUT_PULLUP);
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // Initialize GPS
  gpsPort.begin(9600);
  Serial.println(F("GPS Initialized"));

  Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");

  FastLED.addLeds<SK9822, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
  set_leds(CRGB::Yellow);

}

void set_leds(CRGB color){
  FastLED.clear();
  for(int i = 0; i < NUM_LEDS; i++){
    leds[i] = color;
  }
  FastLED.show();
}

void startNewFile() {
  // Find next available filename
  do {
    filename = "LOG" + String(fileCounter) + ".txt";
    fileCounter++;
  } while (SD.exists(filename));
  
  // Open the new file
  dataFile = SD.open(filename, FILE_WRITE);
  
  // Write the header
  if (dataFile) {
    dataFile.println("timestamp,lat,lon,analog1,analog2,analog3,analog4");
    dataFile.close();
    Serial.println("Created new file: " + filename);
  }
}

bool updateGPS() {
  gpsValid = false;
  if (gps.available(gpsPort)) {
    fix = gps.read();
    if (fix.valid.location) {
      gpsValid = true;
      Serial.println("GPS LOCKED");
      set_leds(CRGB::Green);
    } else {
      Serial.println("GPS data not valid");
      set_leds(CRGB::Yellow);
    }
  }
  return gpsValid;
}

void loop() {
  // Update GPS data
  updateGPS();
  
  // Check buttons (remember they're inverted because of INPUT_PULLUP)
  if (digitalRead(startButton) && !isLogging && gpsValid) {
    isLogging = true;
    startNewFile();
    set_leds(CRGB::Red);
    delay(200); // Simple debounce
  }
  
  if (digitalRead(stopButton) && isLogging) {
    isLogging = false;
    Serial.println("Logging stopped");
    set_leds(CRGB::Blue);
    delay(2000); // Simple debounce
  }
  
  if (isLogging && gpsValid) {
    // make a string for assembling the data to log:
    String dataString = "";
    
    // Add timestamp from GPS if available, otherwise use millis()
    if (fix.valid.time) {
      // Format: HHMMSS.SSS
      dataString += fix.dateTime.hours;
      dataString += fix.dateTime.minutes;
      dataString += fix.dateTime.seconds;
      dataString += ".";
      dataString += fix.dateTime_ms();
    } else {
      dataString += String(millis());
    }
    dataString += ",";
    
    // Add GPS data if valid, otherwise add placeholder values
    if (gpsValid) {
      dataString += String(fix.latitude(), 6);
      dataString += ",";
      dataString += String(fix.longitude(), 6);
    } else {
      dataString += "0.000000,0.000000";
      set_leds(CRGB::Yellow);
    }
    dataString += ",";
    
    // read four sensors and append to the string:
    for (int analogPin = 0; analogPin < 4; analogPin++) {
      int sensor = analogRead(analogPin);
      dataString += String(sensor);
      if (analogPin < 3) {
        dataString += ",";
      }
    }

    // open the file
    dataFile = SD.open(filename, FILE_WRITE);

    // if the file is available, write to it:
    if (dataFile) {
      dataFile.println(dataString);
      dataFile.close();
      // print to the serial port too:
      Serial.println(dataString);
    } else {
      Serial.println("error opening " + filename);
    }
  }
}