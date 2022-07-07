import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
cv.namedWindow("Filter")
def drawRectangles(frame, contours,area_l_thresh,area_u_thresh):
    x_list=[]
    y_list=[]
    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)
        if cv.contourArea(contour) > area_l_thresh and cv.contourArea(contour) < area_u_thresh:
            cv.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
            cv.putText(frame,"Status: {}".format("Detected"), (10,30), cv.FONT_HERSHEY_SIMPLEX,
                                        1, (0, 0, 255), 3)
            x_list.append((x, x+w))
            y_list.append((y, y+h))
    return x_list, y_list
def nothing():
    pass

cv.createTrackbar("L_H","Filter",0,180,nothing)
cv.createTrackbar("U_H","Filter",180,180,nothing)

cv.createTrackbar("L_S","Filter",0,255,nothing)
cv.createTrackbar("U_S","Filter",255,255,nothing)

cv.createTrackbar("L_V","Filter",0,255,nothing)
cv.createTrackbar("U_V","Filter",255,255,nothing)

while(True):
    ret, frame = cap.read()
    if ret:
        frame_hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

        l_h = cv.getTrackbarPos("L_H","Filter")
        u_h = cv.getTrackbarPos("U_H","Filter")

        l_s = cv.getTrackbarPos("L_S","Filter")
        u_s = cv.getTrackbarPos("U_S","Filter")

        l_v = cv.getTrackbarPos("L_V","Filter")
        u_v = cv.getTrackbarPos("U_V","Filter")

        l_bound_hsv = np.array([l_h,l_s,l_v])
        u_bound_hsv = np.array([u_h,u_s,u_v])

        mask = cv.inRange(frame_hsv, l_bound_hsv, u_bound_hsv)

        cv.imshow("frame_hsv",frame_hsv)
        cv.imshow("mask",mask)
        res = cv.bitwise_and(frame_hsv,frame_hsv,mask=mask)
        cv.imshow("res",res)
    else:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    key = cv.waitKey(24)
    if key==27:
        break
cap.release()
cv.destroyAllWindows()



def findContours(frame,l_bound,u_bound,
                        dilate=True,
                        dilate_iteration = 1,
                        draw_contours=False,
                        draw_rectangle=True,
                        kernel_size=(5,5),
                        area_thresh=(400,50000)):
    frame_hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame_hsv,l_bound,u_bound)
    kernel = np.ones(kernel_size, np.uint8)
    frame_contoured = frame.copy()
    frame_rectangled = frame.copy()
    if dilate:
        mask_dilated = cv.dilate(mask, kernel, iterations=dilate_iteration)
        contours, _ = cv.findContours(mask_dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    else:
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if draw_contours:
        cv.drawContours(frame_contoured, contours, -1, (255, 0, 0), 2)
    if draw_rectangle:
        x_list, y_list = drawRectangles(frame_rectangled,
                                                                            contours,
                                                                            area_l_thresh = area_thresh[0],
                                                                            area_u_thresh = area_thresh[1])

    return frame_rectangled, frame_contoured, frame_hsv, mask, x_list, y_list



def findContoursLive(self,dilate=True,
                        l_bound=np.array([0,0,0]),
                        u_bound=np.array([0,0,0]),
                        draw_contours=False,
                        draw_rectangle=True,
                        filter_type="hsv",
                        line=True,
                        area_thresh=(400,50000),
                        dilate_iteration=1,
                        hough_circles=True):
    cap = cv.VideoCapture(self.vid_name)
    if filter_type == "hsv":
        while(True):
            ret, frame = cap.read()
            if ret:
                    frame_rectangled, frame_contoured, frame_hsv, mask, xs, ys = findContours( frame,
                                                                                                        l_bound=l_bound,
                                                                                                        u_bound=u_bound,
                                                                                                        filter_type="hsv",
                                                                                                        area_thresh=area_thresh,
                                                                                                        draw_contours=draw_contours,
                                                                                                        dilate_iteration=dilate_iteration,
                                                                                                        )
            if line:
                frame_rectangled_lined = self.drawLineRect(frame_rectangled,xs,ys)
                cv.imshow("frame_rectangled_lined",frame_rectangled_lined)
            else:
                cv.imshow("frame_rectangled", frame_rectangled)
            if hough_circles:
                frame_circled = frame.copy()
                res = cv.bitwise_and(frame,frame,mask=mask)
                frame_gray = res[:,:,2]
                frame_gray = cv.medianBlur(frame_gray, 5)
                circles = cv.HoughCircles(frame_gray,
                                                    cv.HOUGH_GRADIENT, 1, 10,
                                                    param1=100,
                                                    param2=15,
                                                    minRadius=5,
                                                    maxRadius=20)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for i in circles[0, :]:
                        center = (i[0], i[1])
                        # circle center
                        cv.circle(frame_circled, center, 1, (0, 100, 100), 3)
                        if line:
                            # draw line to the center
                            frame_circled = Detector.drawLine(frame_circled,center)
                        # circle outline
                        radius = i[2]
                        cv.circle(frame_circled, center, radius, (255, 0, 255), 3)
                cv.imshow("frame_circled",frame_circled)
            #cv.imshow("frame", frame)
            #cv.imshow("mask",mask)
            #cv.imshow("frame_hsv",frame_hsv)
            #cv.imshow("frame_contoured",frame_contoured)    
            else:
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            key = cv.waitKey(24)
            if key==27:
                break
    cap.release()
    cv.destroyAllWindows()