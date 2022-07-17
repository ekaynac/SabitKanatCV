#!/usr/bin/env python3 

import cv2 
import numpy as np 
import time

#fx = camera_matrix[0][0]

#def dist(px_length=None):
#    return (px_length/fx)*31



camera_matrix = np.array([[833.1055638, 0, 646.01487175],
                          [0, 833.81159297, 442.18691016],
                          [0,      0,            1      ]])

dist_coefs = np.array([[-0.36237029, 0.18036004, 0.00360551, -0.00120724, -0.05532555]])

newcamera_matrix = np.array([[474.05444336, 0, 653.18944748],
                             [0, 583.01477051, 446.30434518],
                             [0,      0,            1      ]])

x, y, w, h = 286, 137, 728, 511

mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, dist_coefs, None, newcamera_matrix, (1280,720), 5)

a1_unclb=cv2.imread("a1.png")

undst = cv2.remap(a1_unclb, mapx, mapy, cv2.INTER_LINEAR)
undst = undst[y:y+h, x:x+w]
dst = a1_unclb

cv2.imwrite("kalibre.png", undst)
cv2.imwrite("kalibre edilmemiş.png", dst)



