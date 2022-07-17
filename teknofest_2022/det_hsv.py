#!/usr/bin/env python3 

import cv2
import numpy as np

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=360,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )



cap = cv2.VideoCapture(gstreamer_pipeline(sensor_id=0, flip_method=0), cv2.CAP_GSTREAMER)

def nothing(x):
    pass

cv2.namedWindow('tracking')

cv2.createTrackbar("LH", 'tracking', 0, 255, nothing)
cv2.createTrackbar("LS", 'tracking', 0, 255, nothing)
cv2.createTrackbar("LV", 'tracking', 0, 255, nothing)
cv2.createTrackbar("UH", 'tracking', 255, 255, nothing)
cv2.createTrackbar("US", 'tracking', 255, 255, nothing)
cv2.createTrackbar("UV", 'tracking', 255, 255, nothing)

while cap.isOpened():

    ret, frame = cap.read()
    print(frame.shape)
    frame = cv2.resize(frame, (640, 480), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("LH", "tracking")
    l_s = cv2.getTrackbarPos("LS", "tracking")
    l_v = cv2.getTrackbarPos("LV", "tracking")
    u_h = cv2.getTrackbarPos("UH", "tracking")
    u_s = cv2.getTrackbarPos("US", "tracking")
    u_v = cv2.getTrackbarPos("UV", "tracking")

    l_b = np.array([l_h, l_s, l_v]) # found_candidates to be np.array([0, 100, 220])
    u_b = np.array([u_h, u_s, u_v]) # found_candidates to be np.array([255, 255, 255])



    mask1 = cv2.inRange(hsv, l_b, u_b)

    final_frame = cv2.bitwise_and(frame, frame, mask = mask1)

    cv2.imshow('mask', mask1)
    cv2.imshow('frame', frame)
    cv2.imshow('final_frame', final_frame)
    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
