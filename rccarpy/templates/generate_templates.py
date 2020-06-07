import random
import os
import cv2
import numpy as np


def random_noise(image):
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

def horizontal_flip(image):
    flipped = cv2.flip(image, 0)
    return flipped

def rotate(image):
	
	deg = random.randint(0, 120)
	rows = image.shape[0]
	cols = image.shape[1]
	print(rows, cols)
	M = cv2.getRotationMatrix2D((cols / 2, rows / 2), deg, 2)
	img_rot = cv2.warpAffine(image, M, (cols, rows))
	return img_rot


image = cv2.imread('sample.jpg')
#image = cv2.resize(image, (1024, 768 ))
modified = rotate(image)
flip = horizontal_flip(image)
noise_img = random_noise(image)
cv2.imwrite('saved.jpg', noise_img)
cv2.imshow("img", noise_img)
cv2.waitKey()