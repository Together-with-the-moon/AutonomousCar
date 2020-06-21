import cv2
import numpy as np
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
from PIL import Image
import glob

# # initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(640, 480))
# # allow the camera to warmup
# time.sleep(0.1)

def detect_stopSign(image):
    stopSignCascade = cv2.CascadeClassifier('stopsign_classifier.xml')
    print(stopSignCascade.load('stopsign_classifier.xml'))
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    dist_Stop = -100

    try:
      stopSigns = stopSignCascade.detectMultiScale(gray, 1.3, 5)
      print(stopSigns)

      for (x,y,w,h) in stopSigns:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
        cv2.putText(image, "Stop Sign", (x,y), 0, 1, color=(0,0,255), thickness=2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        dist_Stop = (-1.07)*w + 102.597
        cv2.putText(image, f"dist_Stop = {dist_Stop}cm", (1,50), 0, 1, color=(0,0,255), thickness=2)

    except:
     print(" 34DS")

    #print(dist_Stop)
    return  image, dist_Stop

for filename in glob.glob('images/*.jpg'):
    img = Image.open(filename)
    imgArr = np.array(img)
    imgBGR = cv2.cvtColor(imgArr, cv2.COLOR_RGB2BGR)
    detImg, dist_Stop = detect_stopSign(imgBGR)
    cv2.imshow("image", detImg)
    cv2.waitKey(0)

# # capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     # grab the raw NumPy array representing the image, then initialize the timestamp
#     # and occupied/unoccupied text
#     image = frame.array
#     # show the frame
#     detect_stopSign(image)
#     cv2.imshow('stopSign', image)
#     cv2.imshow('Frame', image)
#     key = cv2.waitKey(1) & 0xFF
#     # clear the stream in preparation for the next frame
#     rawCapture.truncate(0)
#     if key == ord("q"):
#         break
