# -*- coding:utf-8 -*-

import numpy as np
import os, cv2, random

_color = [255, 125]

def imcr(i):
        NWLS = []
	if True:
	        im_w, im_h  = i.shape
                w, h = im_w//16, im_h//16
		w_num, h_num = int(im_w/w), int(im_h/h)
                num = 0
		for wi in range(0, w_num):
		    for hi in range(0, h_num):
                        num += 1
                        if wi % 2 and hi%2:
                                i[wi*w:(wi+1)*w, hi*h:(hi+1)*h] = 255#random.choice(_color)
                                print i[wi*w:(wi+1)*w, hi*h:(hi+1)*h].shape

        return np.array(i)

def imgs(x):
      cv2.imshow('Rotat', np.array(x, dtype=np.uint8))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

newImg = np.zeros([586, 586])
kernal = np.zeros([26, 26, 256])
for ixx in range(0, 1):
             for iXx in range(0, 1):
                 step = 0 
                 w = 0
                 h = 0
                 size = 26
                 for mX in range(0, 416, 36):
                     for mY in range(0, 416, 36):
                       newImg[mY+5:mY+(36-5), mX+5:mX+(36-5)] = random.choice(_color)#kernal[:,:,step]#kernal[:,:,iXx]
                 imgs(newImg)
			

def chunks(lst, count):
    start = 0
    for i in range(count):
          stop = start + len(lst[i::count])
          yield lst[start:stop]
          start = stop 
test = chunks(temp_list,40)			
