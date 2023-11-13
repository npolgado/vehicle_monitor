# import re
# import subprocess

# device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
# df = subprocess.check_output("lsusb")
# devices = []
# for i in df.split(b'\n'):
#     if i:
#         info = device_re.match(i)
#         if info:
#             dinfo = info.groupdict()
#             dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
#             devices.append(dinfo)
            
# # print(devices)

# for name in devices:
#     if "Arduino" in str(name["tag"]): print(name['device'])

#########################################################################################

# import os
# import serial.tools.list_ports


# imu_port = list(serial.tools.list_ports.grep("Inertial"))
# if not imu_port: pass
# else:
#     for p in imu_port:
#         imu_port = str(p).split(" - ")[0]
#         break
#     os.environ["IMU_PORT"] = imu_port


# arduino_port = list(serial.tools.list_ports.grep("Arduino"))
# if not arduino_port: pass
# else:
#     for p in arduino_port:
#         arduino_port = str(p).split(" - ")[0]
#         break
#     os.environ["ARDUINO_PORT"] = arduino_port

# if __name__ == "__main__":
#     print("hello")

#########################################################################################

import rospy
import roslaunch
import subprocess
import os
import time
import RPi.GPIO as GPIO
import yaml
import signal
import sys

DATA_PATH = '/media/ubuntu/T7'


def log(msg):
    print(f"[CONTROLS]: {msg}")

def set_imu_config():
    imu_config = '/home/ubuntu/catkin_ws/src/vehicle_monitor/config/imu.yaml'
    with open(imu_config) as f: list_doc = yaml.safe_load(f)
    if os.environ["IMU_PORT"] in list_doc["port"]: log("IMU PORT CORRECT in yaml")
    else: 
        list_doc["port"] = os.environ["IMU_PORT"]
        log("set new IMU config")
        with open(imu_config, "w") as f: yaml.dump(list_doc, f)

def parse_ports(ports):
    ard_port = None
    imu_port = None

    for p in ports:

        if "Arduino" in p and "(USB)" in p:
            ard_port = p.split(" ")[0]
            os.environ["ARDUINO_PORT"] = ard_port
            continue
        
        if "Unknown" in p and "(USB)" in p:
            imu_port = p.split(" ")[0]
            os.environ["IMU_PORT"] = imu_port
            set_imu_config()
            continue

        if ard_port and imu_port: return 1

    return 0

def check_data_drive():
    # check if DATA_PATH exists
    if os.path.exists(DATA_PATH)
        if os.path.ismount(DATA_PATH):
            return True
        else:
            # need to mount drive
            return False
    return False

def launch_data_collection():
    log("launching bringup!")
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/ubuntu/catkin_ws/src/vehicle_monitor/launch/bringup.launch"])
    launch.start()
    return launch

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.IN)

    # log("Checking arduino-cli (this may take several seconds)...")
    # df = subprocess.check_output(["arduino-cli", "board", "list"])
    # ports = df.decode('utf-8').split("\n")
    # status = parse_ports(ports)

    # if status: 
    #     launch = launch_data_collection()
    #     time.sleep(5)
    # else: 
    #     log("no port assignments found :(")
    #     raise ValueError

    switch_state = False
    
    try:
        while True: 
            switch = GPIO.input(2) # this will be 1 when in OFF position and 0 in ON position (inverse bool)
            log(f"got = {switch}")

            try:
                # if the switch is flipped ON but previously OFF
                if not switch and not switch_state: 
                    log("starting to record")
                    if check_data_drive():
                        process = subprocess.Popen(['rosbag', 'record', '-a', '-o', '/home/ubuntu/data_collect.bag'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        switch_state = not switch_state
                
                # if the switch is flipped OFF but previously ON
                elif switch and switch_state:
                    log("stopping recording")
                    process.terminate()
                    switch_state = not switch_state

            except Exception as e:
                print(e)

            time.sleep(1)
            
    except KeyboardInterrupt:
        sys.exit()
