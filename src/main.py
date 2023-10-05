# vehicle ride height and IMU data collection
import time
import os, sys
import serial
from datetime import datetime


storage_path = "/media/admin/T7"

# Define serial port settings
imu_port = "/dev/ttyACM1"
arduino_port = "/dev/ttyACM0"
imu_baudrate = 115200
arduino_baudrate = 9600

# Define output file name
output_file = "data_log.csv"
output_path = os.path.join(storage_path, output_file)

# Define the desired writing speed (in seconds)
write_interval = 1  # Write data every 1 second

# Open serial ports
imu_serial = serial.Serial(imu_port, imu_baudrate)
arduino_serial = serial.Serial(arduino_port, arduino_baudrate)

if __name__ == "__main__":
    # print("Hello World!")

    while True:
        print("IMU")
        print(imu_serial.readline())
        print("\nArduino\n")
        print(arduino_serial.readline())
        time.sleep(1)

    # # Open output file
    # with open(output_path, "w") as file:
    #     try:
    #         file.write(f"TIME,IMU,RIDEHEIGHT\n")
    #         while True:
    #             # Read data from IMU
    #             imu_data = imu_serial.readline().decode().strip()

    #             # Read data from Arduino
    #             arduino_data = arduino_serial.readline().decode().strip()

    #             # Get current timestamp
    #             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    #             # Write data to the output file with timestamp
    #             file.write(f"{timestamp},{imu_data},{arduino_data}\n")
    #             file.flush()  # Flush the buffer to ensure data is written immediately

    #             # Wait for the specified interval
    #             time.sleep(write_interval)

    #     except KeyboardInterrupt:
    #         print("Logging stopped by user.")

    # Close serial ports
    # imu_serial.close()
    arduino_serial.close()

