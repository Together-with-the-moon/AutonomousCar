import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
# Same command function as streaming, its just now we pass in the file path, nice!
cap = cv2.VideoCapture('/Users/2018A00587/Desktop/embedded_system/stopsignvideo.mp4')

# FRAMES PER SECOND FOR VIDEO
fps = 15

def detect_stopSign(image):
    dist_Stop = "unknown"
    stopSignCascade = cv2.CascadeClassifier('stopsign_classifier.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    try:
        stopSigns = stopSignCascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in stopSigns:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
            cv2.putText(image, "Stop Sign", (x,y), 0, 1, color=(0,0,255), thickness=2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            dist_Stop = (-1.07)*w + 102.597
            cv2.putText(image, f"dist_Stop = {dist_Stop}cm", (1,50), 0, 1, color=(0,0,255), thickness=2)

    except:
        print(" 34DS")

    print(dist_Stop)
    return  image, dist_Stop


# Always a good idea to check if the video was acutally there
# If you get an error at thsi step, triple check your file path!!
if cap.isOpened()== False: 
    print("Error opening the video file. Please double check your file path for typos. Or move the movie file to the same location as this script/notebook")
    
# While the video is opened
while cap.isOpened():
    
    # Read the video file.
    ret, frame = cap.read()
    
    # If we got frames, show them.
    if ret == True:
        
        detFrame, dist_Stop = detect_stopSign(frame)
        cv2.imshow('detFrame', detFrame)

         # Display the frame at same frame rate of recording
        # Watch lecture video for full explanation
        time.sleep(1/fps)
        cv2.imshow('frame',frame)
 
        # Press q to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):           
            break
 
    # Or automatically break this whole loop if the video is over.
    else:
        break
        
cap.release()
# Closes all the frames
cv2.destroyAllWindows()