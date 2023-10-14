#!/usr/bin/env python
import rospy
import serial
from std_msgs.msg import Int64, Int16

ARDUINO_STOP_BIT = 0xABC

def parse_serial_data(ser):
    rospy.init_node('serial_reader_node', anonymous=True)
    
    # Create a dictionary to map wheel names to their corresponding masks
    wheel_topics = {
        "front_left": 0xFFF,
        "front_right": 0xFFF000,
        "rear_left": 0xFFF000000,
        "rear_right": 0xFFF000000000,
    }

    # Create publishers for each wheel topic
    publishers = {}
    for wheel, mask in wheel_topics.items():
        topic_name = "rideheight/" + wheel
        publishers[wheel] = rospy.Publisher(topic_name, Int16, queue_size=10)

    stop_bit_received = False
    while not rospy.is_shutdown() and not stop_bit_received:
        data = ser.read(8)  # Assuming 8 bytes for Int64 data
        if len(data) == 8:
            int64_value = int.from_bytes(data, byteorder='little', signed=True)
            for wheel, mask in wheel_topics.items():
                topic_name = "rideheight/" + wheel
                wheel_value = (int64_value & mask) >> (list(wheel_topics.keys()).index(wheel) * 12)
                publishers[wheel].publish(wheel_value)

            # Check for a stop condition (e.g., a specific value in the data)
            if int64_value == ARDUINO_STOP_BIT:
                stop_bit_received = True

if __name__ == '__main__':
    try:
        port = '/dev/ttyACM0'  # Change this to your Arduino's serial port
        baud_rate = 9600  # Change this to match your Arduino's baud rate
        ser = serial.Serial(port, baud_rate)
        parse_serial_data(ser)
    except rospy.ROSInterruptException:
        pass
