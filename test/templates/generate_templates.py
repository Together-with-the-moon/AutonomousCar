import random
import cv2
import numpy as np
from time import sleep



def rand_noise(image):
	rows = image.shape[0]
	cols = image.shape[1]
	mean = 0
	var = 10
	sigma = var ** 0.5
	gaussian = np.random.normal(mean, sigma, (rows, cols)) #  np.zeros((224, 224), np.float32)

	noisy_image = np.zeros(image.shape, np.float32)

	if len(image.shape) == 2:
	    noisy_image = img + gaussian
	else:
	    noisy_image[:, :, 0] = image[:, :, 0] + gaussian
	    noisy_image[:, :, 1] = image[:, :, 1] + gaussian
	    noisy_image[:, :, 2] = image[:, :, 2] + gaussian

	cv2.normalize(noisy_image, noisy_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)
	noisy_image = noisy_image.astype(np.uint8)
	return noisy_image

def rotate(image):

	deg = random.randint(-90, 90)
	rows = image.shape[0]
	cols = image.shape[1]
	#print(rows, cols)
	M = cv2.getRotationMatrix2D((cols / 2, rows / 2), deg, 2)
	img_rot = cv2.warpAffine(image, M, (cols, rows))

	return img_rot

def reSize(image):
	h,w = image.shape[0], image.shape[1]
	print(h,w)
	rand_val = random.randint(-100, 100)
	resized = cv2.resize(image, ((h+rand_val), (w+rand_val)))
	return resized

def flipped(image):
	flippedImage = np.flip(image, 1)
	return flippedImage

image = cv2.imread('template.jpg')

for i in range(1,21): #180 rotations 180 pics
	modifiedImg = rotate(image)
	resizedImg = reSize(image)
	noisyImg = rand_noise(image)
	cv2.imwrite(f'generated_template_Images/saved_{i}.jpg', noisyImg)
	cv2.imwrite(f'generated_template_Images/saved_{i+20}.jpg', modifiedImg)
	cv2.imwrite(f'generated_template_Images/saved_{i+40}.jpg', resizedImg)
	#cv2.imshow("img", modified)

	#sleep(1)
cv2.imshow('winname', image)
fimg = flipped(image)
cv2.imshow('f', fimg)
# cv2.imshow('oo', image[::-1])

cv2.waitKey()