#!/usr/bin/env python3 

import numpy
import cv2
from threading import Thread
import os 


class frame_get:
    def __init__(self):
        self.stopped = False

        self.stream_0 = cv2.VideoCapture((
        "nvarguscamerasrc sensor-id=%d !" "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            0,
            1920,
            1080,
            30,
            0,
            480,
            270,
        )), cv2.CAP_GSTREAMER)

        self.stream_1 = cv2.VideoCapture((
        "nvarguscamerasrc sensor-id=%d !" "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            1,
            1920,
            1080,
            30,
            0,
            480,
            270,
        )), cv2.CAP_GSTREAMER)

        self.grabbed_0, self.frame_0 = self.stream_0.read()
        self.grabbed_1, self.frame_1 = self.stream_1.read()

    
   

    def start(self):
        Thread(target=self.get_0, args=()).start()
        Thread(target=self.get_1, args=()).start()
        return self
     
    def get_0(self):
        while not self.stopped:
            try:
                if not self.grabbed_0:
                    self.stop()
                    break
                else:
                    (self.grabbed_0, self.frame_0) = self.stream_0.read()
            except KeyboardInterrupt: break


    
    def get_1(self):
        while not self.stopped:
            try:
                if not self.grabbed_1:
                    self.stop()
                    break
                else:
                    (self.grabbed_1, self.frame_1) = self.stream_1.read()
            except KeyboardInterrupt: break

    def stop(self):
        self.stopped = True

main_thread = frame_get().start()

while (main_thread.grabbed_0 and main_thread.grabbed_1):
    try:
        frame_0 = main_thread.frame_0
        frame_1 = main_thread.frame_1
        cv2.imshow("sex0", frame_0)
        cv2.imshow("sex1", frame_1)
        if cv2.waitKey(1) == ord("q"):
            break
    except KeyboardInterrupt:
        os.system("sudo service nvargus-daemon restart")
        break
    
