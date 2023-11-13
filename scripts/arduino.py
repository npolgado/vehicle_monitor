#!/usr/bin/env python
import rospy
import serial
from std_msgs.msg import Int64, Int16
import os
import time

ARDUINO_STOP_BIT = 3030

def parse_serial_data(ser):
    rospy.init_node('serial_reader_node', anonymous=True)
    
    # Create 4 topics for each wheel with the namespace "rideheight"
    pub_fl = rospy.Publisher('rideheight/fl', Int16, queue_size=10)
    pub_fr = rospy.Publisher('rideheight/fr', Int16, queue_size=10)
    pub_rl = rospy.Publisher('rideheight/rl', Int16, queue_size=10)
    pub_rr = rospy.Publisher('rideheight/rr', Int16, queue_size=10)

    rate = rospy.Rate(10) # 10hz

    data = [
        0, # fl
        0, # fr
        0, # rl
        0  # rr
    ] 
    index = 0

    while not rospy.is_shutdown():
        # read in serial data until newline
        try:
            line = ser.readline()
            val = int(line)
        except Exception as e:
            val = None
            print(e)
        
        # check if the stop bit is received
        if val == ARDUINO_STOP_BIT and index > 3:
            # print("SENDING")

            # send data to topics
            pub_fl.publish(data[0])
            pub_fr.publish(data[1])
            pub_rl.publish(data[2])
            pub_rr.publish(data[3])
            
            # reset
            # rate.sleep()
            data = [0, 0, 0, 0]
            index = 0

        elif index <= 3:
            data[index] = val
            # print(data)
            index += 1            

if __name__ == '__main__':
    try:
        #port = os.environ["ARDUINO_PORT"]  # Change this to your Arduino's serial port
        port = "/dev/ttyACM1"
        baud_rate = 9600  # Change this to match your Arduino's baud rate
        ser = serial.Serial(port, baud_rate)
        parse_serial_data(ser)
    except rospy.ROSInterruptException:
        pass
