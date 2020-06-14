import cv2
import numpy as np
import time



def match(image, template):
    max_found = 0.0
    ans = 0
    max_vals = [None] * 10
    for i in range(10):
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        max_vals[i] = max_val
       
        if max_val > max_found:
            max_found = max_val
            ans = i

    return (ans, max_found, max_vals) 

pts1 = np.array([[62,135],[340,135],[45,185],[362,185]],np.int32)
pts2 = np.array([[100,0],[280,0],[100,240],[280,240]],np.int32)

def roi():
	pass
	
coord1 = []
coord2 = []


img = cv2.imread('jerry.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

template = cv2.imread('jerryFace.jpg',0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
match(img_gray, template)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

cv2.imshow('Stop Sign',img)
cv2.waitKey(0)