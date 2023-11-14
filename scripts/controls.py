import subprocess
import os
import time
import RPi.GPIO as GPIO
import sys

DATA_PATH = '/media/ubuntu/T7'

def log(msg):
    print(f"[CONTROLS]: {msg}")

def check_data_drive():
    # check if DATA_PATH exists
    if os.path.exists(DATA_PATH):
        if os.path.ismount(DATA_PATH):
            return True
        else:
            log(f"{DATA_PATH} is not mounted, please mount it and try again")
            return False
    return False

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.IN)

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
