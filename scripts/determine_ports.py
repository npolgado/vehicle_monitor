import subprocess
import os
import sys

def find_arduino_port(data, target_string):
    for line in data.split('\n'):
        if target_string in line:
            parts = line.split()
            if parts: return parts[0]

    return None

def find_imu_port(arduino_port):
    if arduino_port == None:
        return None
    try:
        result = subprocess.check_output(
            "ls -a -l /dev | grep ACM",
            shell=True,
            text=True
        ).strip()

        for line in result.split('\n'):
            if arduino_port not in line: return line

    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    print("listing boards...")
    output = subprocess.check_output(["arduino-cli", "board", "list"], text=True)
    target = "arduino:avr:uno"

    print("determining ports...")
    arduino_port = find_arduino_port(output, target)
    imu_port = find_imu_port(arduino_port)

    if arduino_port == None or imu_port == None:
        print("ERROR FINDING PORTSSS >:(")
        sys.exit()

    print("setting environment...")
    os.environ["ARDUINO_PORT"] = arduino_port
    os.environ["IMU_PORT"] = imu_port

    print("sys bringup down!")
    sys.exit()