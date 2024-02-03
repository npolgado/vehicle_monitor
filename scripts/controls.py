import subprocess
import os
import time
import sys

# TODO: this requires a screen to be active for the window...
import pygame
pygame.init()

# TODO: fix FSTAB to mount the drive on boot
DATA_PATH = '/media/ubuntu/T7'

def log(msg): print(f"[CONTROLS]: {msg}")

def check_data_drive():
    # check if DATA_PATH exists
    if os.path.exists(DATA_PATH) and os.path.ismount(DATA_PATH): return True
    log(f"{DATA_PATH} is not mounted, please mount it and try again")
    return False

if __name__ == "__main__":
    switch_state = False
    display = pygame.display.set_mode((100, 100))

    try:
        while True:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print("A key has been pressed")
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            display.fill((255, 255, 255))

            pygame.display.flip()

    finally: 
        pygame.quit()