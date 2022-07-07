import cv2 as cv
import numpy as np
from detector import *

front_cap = cv.VideoCapture(r"D:\GitHub\SabitKanatCV\RedDetection\reddetection.mp4")
main_cap = cv.VideoCapture(0)

kernel_dilation = np.ones(5, np.uint8)
kernel_erosion = np.ones(5, np.uint8)

lower1 = np.array([0,100,20])
upper1 = np.array([10,255,255])

lower2 = np.array([160,100,20])
upper2 = np.array([179,255,255])

while(True):
    ret, frame_front = front_cap.read()
    ret, frame_main = main_cap.read()
    if ret:
        frame_front_hsv = cv.cvtColor(frame_front,cv.COLOR_BGR2HSV)
        frame_main_hsv = cv.cvtColor(frame_main,cv.COLOR_BGR2HSV)

        frame_front_hsv_blured = cv.GaussianBlur(frame_front_hsv,(15,15),2)
        frame_main_hsv_blured = cv.GaussianBlur(frame_main_hsv,(15,15),2)

        mask1_main = cv.inRange(frame_main_hsv_blured,lower1,upper1)
        mask1_front = cv.inRange(frame_front_hsv_blured,lower1,upper1)
        mask2_main = cv.inRange(frame_main_hsv_blured,lower2,upper2)
        mask2_front = cv.inRange(frame_front_hsv_blured,lower2,upper2)

        mask_front = mask1_front + mask2_front
        mask_main = mask1_main + mask2_main

        mask_front_refined = cv.erode(mask_front, kernel_erosion, iterations=10)
        mask_main_refined = cv.erode(mask_main, kernel_erosion, iterations=10)

        mask_front_refined = cv.dilate(mask_front_refined, kernel_dilation, iterations=5)
        mask_main_refined = cv.dilate(mask_main_refined, kernel_dilation, iterations=5)

        front_contours, _ = cv.findContours(mask_front_refined, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        main_contours, _ = cv.findContours(mask_main_refined, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        frame_front, front_x_list, front_y_list = cvDetector.drawRectangle(frame_front, front_contours, area_thresh= (1000, 50000),
                                                                            rectangle_color=(255,0,0), rectangle_thickness=2)
        frame_main, main_x_list, main_y_list = cvDetector.drawRectangle(frame_main, main_contours, area_thresh= (1000, 50000),
                                                                            rectangle_color=(255,0,0), rectangle_thickness=2)

        frame_main = cvDetector.distfromcenter(frame_main, main_x_list, main_y_list)
        frame_front = cvDetector.distfromcenter(frame_front, front_x_list, front_y_list)
        
        cv.imshow("front",frame_front)
        cv.imshow("main",frame_main)
        cv.imshow("mask_front_refined",mask_front_refined)
        cv.imshow("mask_main_refined",mask_main_refined)
    else:
        front_cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    key = cv.waitKey(24)
    if key==27:
        break