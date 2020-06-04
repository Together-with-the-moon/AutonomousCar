import cv2
from algorithms import *
from setupCam import setup
camera, rawCapture = setup()

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