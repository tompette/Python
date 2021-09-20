import cv2
import numpy as np
from matplotlib import pyplot as plot

#-----------odczyt w skali szarosci--------------------
img1 = cv2.imread('C:/Users/misia/Desktop/mgr/data/2021-09-16_1740.jpg')

img = cv2.resize(img1,None,fx=0.7, fy=0.7, interpolation=cv2.INTER_CUBIC)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#-------PROGROWANIE GLOBALNE------------
ret, img_bin = cv2.threshold(img_gray, 40, 255, cv2.THRESH_BINARY) #bylo: 128
#--------PROGOWANIE ADAPTACYJNE---------
th2 = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

#--------BINARYZACJA OTSU-------------
retval2,threshold2 = cv2.threshold(img_gray,175,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#-------OTWARCIE=DYLATACJA + EROZJA-------------
#retOtsu, imgThresholdedOtsu = cv2.threshold(imgArray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
kernel = np.ones((5,5), np.uint8)
#imgErosion = cv2.erode(threshold2, kernel, iterations = 1)
#imgDilation = cv2.dilate(threshold2, kernel, iterations = 1)
imgOpening = cv2.morphologyEx(threshold2, cv2.MORPH_OPEN, kernel)
#cv2.imshow('first',img_bin)
cv2.imshow('first', threshold2)
cv2.waitKey(0)
cv2.imshow('first', imgOpening)
cv2.waitKey(0)