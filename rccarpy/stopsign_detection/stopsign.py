import cv2
import numpy as np


def detect_stopSign(image):
	stopSignCascade = cv2.CascadeClassifier('stopsign_classifier.xml')
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	stopSigns = stopSignCascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in stopSigns:
	        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
	        roi_gray = gray[y:y+h, x:x+w]
	        roi_color = image[y:y+h, x:x+w]
		cv2.putText(image, 'stopSign', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36,255,12), 2)

	return image
