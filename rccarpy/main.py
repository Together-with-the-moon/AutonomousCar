import cv2
import RPi.GPIO as GPIO

from time import sleep
from algorithms import *
from setupCam import setup
camera, rawCapture = setup()
from motor import *

# motor control pin setting
GPIO.setmode(GPIO.BCM)
print("GPIO OK")
GPIO.setwarnings(False)
pwm1 = setPinConfig(ENA, motor1IN1, motor1IN2)
pwm2 = setPinConfig(ENB, motor2IN1, motor2IN2)
terminatePoint= True
isfirsterror = True
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    imgPers = Perspective(image, pts1)
    imgFinal, imgFinalDuplicate, imgFinalDuplicate1 = Threshold(imgPers)
    histogramLane, laneEnd = Histogram(imgFinalDuplicate, imgFinalDuplicate1)
    LeftLanePos, RightLanePos = LaneFinder(imgFinal, histogramLane)
    Result = LaneCenter(imgFinal, LeftLanePos, RightLanePos)
    image, dist_Stop = detect_stopSign(image)

    if 5 < dist_Stop < 20:
        print("Stop Sign")
        dist_Stop = 0
        # send a stop signal
        setMotor(LeftMotor_front,pwm1,100,dist_Stop)
        sleep(0.003)
        setMotor(RightMotor_front,pwm2,100,dist_Stop)
        sleep(0.01)

    if laneEnd > 12000:
        print("Lane End")
        sleep(1.5)
        setMotor(MOTOR1,pwm1,100,Stop) #left motor operation
        setMotor(MOTOR2,pwm2,100,Stop) #right motor opreation
        sleep(1)
        setMotor(LeftMotor,pwm1,DutyCycle1,Movement1) #left motor operation
        setMotor(RightMotor,pwm2,DutyCycle2,Movement2) #right motor opreation
        sleep(0.001)       
        # send a temporal stop signal
        
    """        
    DutyCycle1 = adjust_PID(error,DutyCycle1)
    DutyCycle2 = adjust_PID(error,DutyCycle2):
    setMotor(LeftMotor,pwm1,DutyCycle1,Movement1)
    setMotor(RightMotor,pwm2,DutyCycle2,Movement2)
    sleep(0.6):
    """
    
    ResList = [laneEnd>12000, Result==0, 0<Result<10, 10<=Result<20, 20<=Result, -10<Result<0, -20<Result<=-10, Result<=-20]
    DirList = ["Lane End", "Forward", "Right1", "Right2", "Right3", "Left1", "Left2", "Left3"]
    
    for Res, Dir in zip(ResList, DirList):
        if ResList[0]:
            print(Dir)
            ss = "Lane End"
            cv2.putText(image, ss, (1,50), 0, 1, color=(255,0,0), thickness=2)
            break
        elif Res:
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
    print("error", Result)

    # CameraBleeding_Filtering
    if isfirsterror:
        if Result >-5 or Result <5 :
            isfirsterror = False
            print("error bye")
            continue 
    
    operation_array_left = isvaildPostion(Result,operation_array_left)
    DutyCycle1,DutyCycle2 = dutyCycle_adjust(PID_control(Result))
    
    length = len(operation_array_left)
            
    #prameter setting
        
    LeftMotor = operation_array_left[length-2:length-1,0:1][0][0]
    RightMotor = operation_array_left[length-1:length,0:1][0][0]
    Movement1 = operation_array_left[0:1,1:2][0][0]
    Movement2 = operation_array_left[1:2,1:2][0][0]
         
    print("DutyCycle1 and DutyCycle2",DutyCycle1,DutyCycle2)  
    setMotor(LeftMotor,pwm1,DutyCycle1,Movement1) #left motor operation
    setMotor(RightMotor,pwm2,DutyCycle2,Movement2) #right motor opreation
    sleep(0.001)

GPIO.cleanup()