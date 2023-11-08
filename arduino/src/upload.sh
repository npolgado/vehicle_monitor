#!bin/sh

echo "Uploading to Arduino"

sleep 1

arduino-cli compile -b arduino:avr:uno ./adc

echo "compiled! uploading now..."
sleep 1

arduino-cli upload ./adc -p $ARDUINO_PORT -b arduino:avr:uno