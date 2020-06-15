import cv2
import RPi.GPIO as GPIO

from time import sleep
from algorithms import *
from setupCam import setup
camera, rawCapture = setup()
from motor import *
from stopsign_detection.stopsign import detect_stopSign

# motor control pin setting
GPIO.setmode(GPIO.BCM)
print("GPIO OK")
GPIO.setwarnings(False)
pwm1 = setPinConfig(ENA, motor1IN1, motor1IN2)
pwm2 = setPinConfig(ENB, motor2IN1, motor2IN2)
pwm3 = setPinConfig(ENC, motor3IN1, motor3IN2)
pwm4 = setPinConfig(END, motor4IN1, motor4IN2)
terminatePoint= True

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    imgPers = Perspective(image, pts1)
    imgFinal, imgFinalDuplicate, imgFinalDuplicate1 = Threshold(imgPers)
    histogramLane = Histogram(imgFinalDuplicate)
    LeftLanePos, RightLanePos = LaneFinder(imgFinal, histogramLane)
    Result = LaneCenter(imgFinal, LeftLanePos, RightLanePos)
#     dist_Stop, image = detect_stopSign(image)

#     if 5 < dist_Stop < 20:
#         print("Stop Sign")
#         dist_Stop = 0
#         # send a stop signal
#         setMotor(LeftMotor_front,pwm1,100,dist_Stop)
#         sleep(0.003)
#         setMotor(RightMotor_front,pwm2,100,dist_Stop)
#         sleep(0.01)
        
    #Motor Control Main_method
    operation_array_left,operation_array_left_right = isvaildPostion(Result,operation_array_left)
    length = len(operation_array_left)
        
    #prameter setting
    LeftMotor_front = operation_array_left[length-2:length-1,0:1][0][0]
    LeftMotor_rear = operation_array_left[length-1:length,0:1][0][0]
    RightMotor_front = operation_array_left_right[length-2:length-1,0:1][0][0]
    RightMotor_rear = operation_array_left_right[length-1:length,0:1][0][0]
    DutyCycle1 = operation_array_left[0:1,2:3][0][0]
    DutyCycle2 = operation_array_left[1:2,2:3][0][0]
    Movement1 = operation_array_left[0:1,1:2][0][0]
    Movement2 = operation_array_left[1:2,1:2][0][0]
     
    setMotor(LeftMotor_front,pwm1,DutyCycle1,Movement)
    sleep(0.003)
    setMotor(RightMotor_front,pwm2,DutyCycle2,Movement)
    sleep(0.01)
    
    print(Movement1)
    print(LeftMotor_front,DutyCycle1,Movement1)
    setMotor(LeftMotor_front,pwm1,DutyCycle1,Movement1)
    setMotor(LeftMotor_rear,pwm2,DutyCycle2,Movement2)
    setMotor(RightMotor_front,pwm3,DutyCycle1,Movement1)
    setMotor(RightMotor_rear,pwm4,DutyCycle2,Movement2)
    sleep(2)

    ResList = [Result==0, 0<Result<10, 10<=Result<20, 20<=Result, -10<Result<0, -20<Result<=-10, Result<=-20]
    DirList = ["Forward", "Right1", "Right2", "Right3", "Left1", "Left2", "Left3"]
    
    for Res, Dir in zip(ResList, DirList):
        if Res:
            print(Dir)
            ss = f"Result = {Result} Move {Dir}"
            cv2.putText(image, ss, (1,50), 0, 1, color=(0,0,255), thickness=2)
            break
        
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    if key == ord("q"):
        break
  
GPIO.cleanup()