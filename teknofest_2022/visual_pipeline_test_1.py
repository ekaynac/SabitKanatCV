#!/usr/bin/env python3 

import cv2 
import numpy as np 
import time

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=30,
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


#fx = camera_matrix[0][0]

#def dist(px_length=None):
#    return (px_length/fx)*31

cap = cv2.VideoCapture(gstreamer_pipeline(sensor_id=0, flip_method=0), cv2.CAP_GSTREAMER)





camera_matrix = np.array([[833.1055638, 0, 646.01487175],
                          [0, 833.81159297, 442.18691016],
                          [0,      0,            1      ]])

dist_coefs = np.array([[-0.36237029, 0.18036004, 0.00360551, -0.00120724, -0.05532555]])

newcamera_matrix = np.array([[474.05444336, 0, 653.18944748],
                             [0, 583.01477051, 446.30434518],
                             [0,      0,            1      ]])

x, y, w, h = 286, 137, 728, 511

mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, dist_coefs, None, newcamera_matrix, (1280,720), 5)



while cap.isOpened():
    
    
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)  # TODO remark the orientation 
    dst = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
    dst = dst[y:y+h, x:x+w]
    cv2.imshow("sex", dst)
    cv2.waitKey(1)
    #h, w = dst.shape[:2]
    #dst = cv2.circle(dst, (int(w/2), int(h/2)), 5, (0,0,255), -1)
    #if cv2.waitKey(1)==ord("q"): 
    #    print(frame.shape)
    #    break



