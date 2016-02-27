__author__ = 'armando'

import numpy as np
import cv2

im = cv2.imread('images/negative_captcha.png')
im[im == 255] = 1
im[im == 0] = 255
im[im == 1] = 0
im2 = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(im2,255,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for i in range(0, len(contours)):
    if (i % 2 == 0):
       cnt = contours[i]
       #mask = np.zeros(im2.shape,np.uint8)
       #cv2.drawContours(mask,[cnt],0,255,-1)
       x,y,w,h = cv2.boundingRect(cnt)
       cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),1)
       cv2.imshow('Features', im)
       cv2.imwrite('images/box_captcha.png', im)

cv2.destroyAllWindows()