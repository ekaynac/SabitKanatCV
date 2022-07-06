import cv2 as cv
import numpy as np
from detector import *

def nothing(a): pass
cv.namedWindow("Filter")
cv.createTrackbar("L_H","Filter",0,180,nothing)
cv.createTrackbar("U_H","Filter",255,180,nothing)

cv.createTrackbar("L_S","Filter",0,255,nothing)
cv.createTrackbar("U_S","Filter",255,255,nothing)

cv.createTrackbar("L_V","Filter",0,255,nothing)
cv.createTrackbar("U_V","Filter",255,255,nothing)

cap = cv.VideoCapture(r"D:\GitHub\SabitKanatCV\RedDetection\reddetection.mp4")

kernel_dilation = np.ones(5, np.uint8)
kernel_erosion = np.ones(5, np.uint8)

while(True):
    ret, frame = cap.read()
    if ret:
        frame_hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

        frame_hsv_blured = cv.GaussianBlur(frame_hsv,(5,5),7)
        
        l_h = cv.getTrackbarPos("L_H","Filter")
        u_h = cv.getTrackbarPos("U_H","Filter")
        
        l_s = cv.getTrackbarPos("L_S","Filter")
        u_s = cv.getTrackbarPos("U_S","Filter")
        
        l_v = cv.getTrackbarPos("L_V","Filter")
        u_v = cv.getTrackbarPos("U_V","Filter")
        
        l_bound = np.array([l_h,l_s,l_v])
        u_bound = np.array([u_h,u_s,u_v])
        
        mask = cv.inRange(frame_hsv,l_bound,u_bound)
        mask_refined = cv.erode(mask, kernel_erosion, iterations=10)
        mask_refined = cv.dilate(mask_refined, kernel_dilation, iterations=5)
        contours, _ = cv.findContours(mask_refined, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        frame, x_list, y_list = cvDetector.drawRectangle(frame, contours, area_thresh= (1000, 50000), rectangle_color=(255,0,0), rectangle_thickness=2)
        frame = cvDetector.distfromcenter(frame, x_list, y_list)
        cv.imshow("frame",frame)
        cv.imshow("frame_hsv",frame_hsv)
        cv.imshow("mask",mask)
        res = cv.bitwise_and(frame_hsv,frame_hsv,mask=mask)
        cv.imshow("mask_refined",mask_refined)
    else:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    key = cv.waitKey(24)
    if key==27:
        break