#!/usr/bin/env python3


import cv2 
import numpy as np 
import time
import serial


def calc(dist_y = 0, focal_length = 833.5055638):
    desired_distance = dist_y*400/focal_length
    return desired_distance 
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



arduino = serial.Serial("/dev/ttyUSB0", 
baudrate=115200,
timeout=5, 
bytesize=serial.EIGHTBITS, 
parity=serial.PARITY_NONE, 
stopbits=serial.STOPBITS_ONE, 
xonxoff = False,
rtscts = False,
dsrdtr = False,
writeTimeout = 2)



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

lower1 = np.array([0, 100, 20])
upper1 = np.array([10, 255, 255])
 
    
 
# upper boundary RED color range values; Hue (160 - 180)
lower2 = np.array([160,100,20])
upper2 = np.array([179,255,255])
 

shape_once = True

while cap.isOpened():
        
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)   
    dst = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
    dst = dst[y:y+h, x:x+w]
    if shape_once :
        height, width, _ = dst.shape
        shape_once = False 
    img_hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(img_hsv, (5,5), 2)
    lower_mask = cv2.inRange(img_hsv, lower1, upper1)
    upper_mask = cv2.inRange(img_hsv, lower2, upper2)
    mask = lower_mask + upper_mask
    refined = cv2.erode(mask, np.ones(5, np.uint8), 10)
    refined = cv2.dilate(refined, np.ones(5, np.uint8), 5)
    contours, _ = cv2.findContours(refined, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = list(contours)
    cv2.rectangle(dst, ((width//2) - 100, (height//2) + 100), ((width//2) + 100, (height//2) - 100), (0, 255, 0), 2)
    
    if len(contours) > 0:
        sorted_contours = max(contours, key=cv2.contourArea)
        M = cv2.moments(sorted_contours)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
	# draw the contour and center of the shape on the image
        cv2.circle(dst, (cX, cY), 2, (255, 0, 0), -1)
        #cv2.drawContours(dst, sorted_contours, -1, (0, 255, 0), 3)
        #print(calc(dist_y=cX-width/2))
        if ((width//2) - 100 < cX) and (cX < (width//2) + 100) and ((height//2) + 100 > cY) and (cY > (height//2) - 100):
            try:
                
                cmd = str(1) + "|"
                arduino.write(cmd.encode())                              
            except Exception as e:
                print(e)
                arduino.close()
        else:
            try:
                pass
                #cmd = str(0) + "|"
                #arduino.write(cmd.encode())                              
            except Exception as e:
                print(e)
                arduino.close()

    cv2.imshow("dst", dst)
    cv2.waitKey(1) 
   




