from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def setup():
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    # resolution 
    camera.resolution = (400, 240)
    # FR
    camera.framerate = 15
    rawCapture = PiRGBArray(camera, size=(400, 240))
    # allow the camera to warmup
    time.sleep(0.1)
    return camera, rawCapture