import cv2
import numpy as np
import time


pts1 = np.array([[62,135],[340,135],[45,185],[362,185]],np.int32)
pts2 = np.array([[100,0],[280,0],[100,240],[280,240]],np.int32)

def roi():
	pass
	
coord1 = []
coord2 = []


img = cv2.imread('generated_template_Images/templates.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

template = cv2.imread('template.jpg',0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

cv2.imshow('Stop Sign',img)
cv2.waitKey(0)