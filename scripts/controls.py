import subprocess
import os
import time
import sys
import keyboard

# TODO: fix FSTAB to mount the drive on boot
DATA_PATH = '/media/ubuntu/T7'

def log(msg): print(f"[CONTROLS]: {msg}")

def check_data_drive():
    # check if DATA_PATH exists
    if os.path.exists(DATA_PATH) and os.path.ismount(DATA_PATH): return True
    log(f"{DATA_PATH} is not mounted, please mount it and try again")
    return False

if __name__ == "__main__":
    # check if the data drive is mounted, if not, throw error, print and exit
    if not check_data_drive():
        log("Exiting the program due to data drive not being mounted...")
        sys.exit(1)

    # params
    recording = False
    race_count = 0
    process = None
    bag_name = f"race_{race_count}.bag"
    bag_path = os.path.join(DATA_PATH, bag_name)
    cmd = f"rosbag record -a -o {bag_path}"

    try:
        while True:
            key_pressed = keyboard.read_key()
            log(f'Key pressed: {key_pressed}')

            # Stop the script when 'esc' is pressed
            if key_pressed == 'esc':
                break
            
            # if 'a' is pressed, start recording
            if key_pressed == 'a':
                if not recording:
                    process = subprocess.Popen(cmd, shell=True)
                    recording = True
                    log(f"Recording started: {bag_name}")
                else:
                    log("Recording already in progress")
            
            # if 'b' is pressed, stop recording, increment the race_count, and update the bag_name, and bag_path
            if key_pressed == 'b':
                if recording:
                    process.terminate()
                    recording = False
                    log(f"Recording stopped: {bag_name}")
                    race_count += 1
                    bag_name = f"race_{race_count}.bag"
                    bag_path = os.path.join(DATA_PATH, bag_name)
                    cmd = f"rosbag record -a -o {bag_path}"

    except Exception as e:
        log(f"Error: {e}")
        sys.exit(1)

    finally: pass