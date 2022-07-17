#!/usr/bin/env python3

import cv2
import time 

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
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

def save_frame():
    window_title = "calibration"

    video_capture = cv2.VideoCapture(gstreamer_pipeline(sensor_id=0, flip_method=0), cv2.CAP_GSTREAMER)

    a = time.time()
    n = 0
 
    if video_capture.isOpened():
        try:
            while True:
                b = time.time()
                ret_val, frame = video_capture.read()
                #frame = cv2.flip(frame, 0)
                if b-a>5:
                    n=n+1
                    name = "a"+str(n) + ".png"
                    if n == 5: break
                    cv2.imwrite(name, frame)
                    print(str(n)+" frame")
                    print(frame.shape)
                    a = time.time()
               
                keyCode = cv2.waitKey(10) & 0xFF
      
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

if __name__ == "__main__":

    save_frame()

