#!/usr/bin/env python3

import numpy as np
import cv2 
import os
import time

pattern_size = (8, 6)
pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)


obj_points = []
img_points = []
h, w = 720, 1280

    
n = 0
image_count=0
image_goal=19
while True:
    n += 1
    img = cv2.imread("a"+str(n)+".png")
    print('Searching for chessboard in frame ' + str(n) + '...')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = img.shape[:2]
    found, corners = cv2.findChessboardCorners(img, pattern_size, flags=cv2.CALIB_CB_FILTER_QUADS)
    if found:
        term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 27, 0.1)
        cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
        image_count=image_count+1
        if image_count==image_goal:
            break
    if True:
        img_chess = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.drawChessboardCorners(img_chess, pattern_size, corners, found)
        cv2.imwrite("calibration_"+str(n)+".png", img_chess)
    if not found:
        print ('not found')
        continue
    img_points.append(corners.reshape(1, -1, 2))
    obj_points.append(pattern_points.reshape(1, -1, 3))

    print ('ok')
    if n == image_goal: break     

print('\nPerforming calibration...')
rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
print ("RMS:", rms)
print ("camera matrix:\n", camera_matrix)
print ("distortion coefficients: ", dist_coefs.ravel())



newcamera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w,h), 1, (w,h))
dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcamera_matrix)
x, y, w, h = roi



file = open("variables.txt", "w+")

file.write("camera matrix : \n" + str(camera_matrix))
file.write("\n dist coefs : \n" + str(dist_coefs))
file.write("\n new camera matrix : \n" + str(newcamera_matrix))
file.write("\n roi (x, y, w, h): \n" + str(np.array([x,y,w,h])))
file.close()

print("\n done calibrating")



"""
to see the distinction in mid point in both dist-undist frames 
"""

"""
h, w = dst.shape[:2]
dst = cv2.circle(dst, (int(w/2), int(h/2)), 5, (0,0,255), -1)
dst = cv2.circle(dst, (int(w/2)+20, int(h/2)), 5, (0,0,255), -1)
cv2.imwrite("sexx.png", dst)
img = cv2.circle(img, (int(width/2), int(height/2)), 5, (0,0,255), -1)
img = cv2.circle(img, (int(width/2)+20, int(height/2)), 5, (0,0,255), -1)
cv2.imwrite("sexxx.png", img)
"""












