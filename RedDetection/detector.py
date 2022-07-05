import cv2 as cv
import time
class cvDetector:
    # Empty function for slider arguments
    @staticmethod
    def nothing(x):
        pass
    # Takes min-max x and y coordinates
    # Returns center coordinates of given rectangle
    @staticmethod
    def rectangleCenter(xs, ys):
        xc = int((xs[0] + xs[1])/2)
        yc = int((ys[0] + ys[1])/2)
        obj_center_coordinate = (xc, yc)
        return obj_center_coordinate
    # Takes a frame (does not change the given argument frame)
    # Takes x's and y's in two ordered arrays
    # Returns a new frame with lines to given coordinates
    @staticmethod
    def distfromcenter(frame, x_list, y_list, line_colour = (0,0,255) , line_thickness = 1, font = cv.FONT_HERSHEY_SIMPLEX):
        frame_lined = frame.copy()
        center_x = int(frame_lined.shape[1]/2)
        center_y = int(frame_lined.shape[0]/2)
        center_coordinate = (center_x, center_y)
        for xs, ys in zip(x_list,y_list):
            obj_center_coordinate = cvDetector.rectangleCenter(xs, ys)
            x_dist = obj_center_coordinate[0] - center_x
            y_dist = obj_center_coordinate[1] - center_y
            cv.line(frame_lined, (0,center_y), (frame_lined.shape[1],center_y), line_colour, line_thickness)
            cv.line(frame_lined, (center_x,0), (center_x,frame_lined.shape[0]), line_colour, line_thickness)
            cv.line(frame_lined, center_coordinate, obj_center_coordinate, line_colour, line_thickness)
            print("X'te uzaklık: {:.2f}\nY'de uzaklık: {:.2f}".format(x_dist,y_dist))
            if x_dist>0:
                print("Nesne çizginin sağında")
            else:
                print("Nesne çizginin solunda")
        return frame_lined
    # Takes a frame (does not change the given argument frame)
    # Takes contours from cv.findContours() method
    # Returns a new frame with rectangles on given contours
    # Returns drawn rectangles' min-max x coordinates and min-max y coordinates
    @staticmethod
    def drawRectangle(frame, contours, area_thresh=(0,50000), rectangle_color=(255,0,0), rectangle_thickness=2):
        area_l_thresh = area_thresh[0]
        area_u_thresh = area_thresh[1]
        frame_rectangled = frame.copy()
        x_list = []
        y_list = []
        for contour in contours:
            (x, y, w, h) = cv.boundingRect(contour)

            if cv.contourArea(contour) > area_l_thresh and cv.contourArea(contour) < area_u_thresh:
                cv.rectangle(frame_rectangled, (x, y), (x+w, y+h), rectangle_color, rectangle_thickness)
                cv.putText(frame_rectangled,"Tespit Edildi", (10,30), cv.FONT_HERSHEY_SIMPLEX,
                                        1, (0, 0, 255), 3)
                x_list.append((x,x+w))
                y_list.append((y,y+h))
        return frame_rectangled, x_list, y_list
    # Takes a frame (does not change the given argument frame)
    # Takes upper and lower bound for mask    
    @staticmethod
    def drawContours(frame,l_bound,u_bound):
        mask = cv.inRange(frame,l_bound,u_bound)
        frame_contoured = frame.copy()
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(frame_contoured, contours, -1, (255, 0, 0), 2)
        return frame_contoured
    # Takes barnames and and its min max positions of bars in "barnames" order
    @staticmethod
    def createTrackbars(barnames, windowname, gaps):
        for barname, gap in zip(barnames,gaps):
            cv.createTrackbar(barname, windowname, gap[0], gap[1], cvDetector.nothing)
    # Gets bar positions in "barnames" order
    @staticmethod
    def getTrackbars(barnames, windowname):
        pos_list = []
        for barname in barnames:
            pos_list.append(cv.getTrackbarPos(barname, windowname))
        return pos_list