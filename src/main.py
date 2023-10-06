# vehicle ride height and IMU data collection
import time
import os, sys
import serial
from datetime import datetime
import yaml

# Load YAML data from the file
with open('config.yaml', 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)

# Access variables from the loaded data
print(f"Script Version: {config['script_version']}")

# SCRIPT PARAMS
DATE = datetime.now().strftime("%Y_%m_%d")
SESSION_FILE_NAME = os.path.join(config["storage_path"], f"data_log_{DATE}.csv")

# Open serial ports
imu_serial = serial.Serial(
    config["imu"]["port"],
    config["imu"]["baudrate"]
)

arduino_serial = serial.Serial(
    config["arduino"]["port"], 
    config["arduino"]["baudrate"]
)

## TODO
def read_arduino():
    # Values from Ride Height 
    # ~100 (0x64)  minumum
    # ~950 (0x3E8) maximum
    data = []
    raw = arduino_serial.readline().decode().strip()
    t_s = time.monotonic() 

    while raw != config["arduino"]["start_bit"]:
        data.append(raw)
        raw = arduino_serial.readline().decode().strip()
        if float(time.monotonic() - t_s) > config["arduino"]["timeout"]: pass

    return data

## TODO
def read_imu():
    raw = imu_serial.readline().decode().strip()
    return raw

if __name__ == "__main__":
    hz = float(1/config["period"])

    print(f"VEHICLE MONITOR")
    print(f"RUNNING DATA COLLECTION AT {hz} HZ")
    time.sleep(1)

    # Open output file
    with open(SESSION_FILE_NAME, "w") as file:
        try:
            # CSV Header
            file.write(f"TIME,IMU,RIDEHEIGHTS\n")
            
            # Main Loop
            while True:
                imu = read_imu()
                print(imu)

                arduino = read_arduino()
                print(arduino)

                timestamp = datetime.now().time().strftime("%H:%M:%S")
                file.write(f"{timestamp},{imu},{arduino}\n")

                # Flush the buffer to ensure data is written immediately
                file.flush()
                time.sleep(config["period"])

        except KeyboardInterrupt:
            print("Logging stopped by user.")
            print("exiting...")
            
            imu_serial.close()
            arduino_serial.close()
            sys.exit()       

