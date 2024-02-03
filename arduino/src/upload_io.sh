#!bin/sh

echo "Uploading to Arduino"

sleep 1

cd /home/ubuntu/catkin_ws/src/vehicle_monitor/arduino/src

arduino-cli compile -b arduino:avr:uno ./io_board

echo "compiled! uploading now..."
sleep 1

arduino-cli upload ./adc -p $ARDUINO_PORT -b arduino:avr:uno