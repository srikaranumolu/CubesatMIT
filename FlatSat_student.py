"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

#AUTHOR: Lunar Loudoun
#DATE: 11/29/2024

#import libraries
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2

#VARIABLES
THRESHOLD = 0      #Any desired value from the accelerometer
REPO_PATH = ""     #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "images"   #Your image folder path in your GitHub repo: ex. /Images

#imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()


def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        origin.pull()
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit('New Photo')
        origin.push()
    except:
        print('Couldn\'t upload to git')


def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = (f'{FOLDER_PATH}/{name}{t}.jpg')
    return imgname


def take_photo():
    """
    This function is NOT complete. Takes a photo when the FlatSat is shaken.
    Replace psuedocode with your own code.
    """
    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        #CHECKS IF READINGS ARE ABOVE THRESHOLD
        if (accely > THRESHOLD or accelx > THRESHOLD or accelz > THRESHOLD):
            picam2.start()
            #PAUSE
            time.sleep(2)
            imgname = img_gen("LunarL")
            #TAKE PHOTO
            picam2.capture_file(imgname)
            #PUSH PHOTO TO GITHUB
            picam2.stop()
            time.sleep(1)
            git_push()
            
        #PAUSE
        time.sleep(2)
        


def main():
    take_photo()


if __name__ == '__main__':
    main()
