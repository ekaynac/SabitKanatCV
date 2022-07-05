import cv2 as cv
from math import radians, cos, sqrt
import numpy as np
class Distance:
    def __init__(self,height,src=0):
        self.distance_px_x = 0 # as px
        self.distance_px_y = 0 # as px
        self.region = 1 # at which region the center of contour is currently needs to be updated each frame
        self.distance= 0 # as m
        self.height = height # as m
        self.angle= 0 # as degree
        self.cap = cv.VideoCapture(src)
        self.focal_lenght=3.04 # as mm
        self.width_px= 640 # as px
        self.height_px= 480 # as px
        self.x_fow_degree = 62.2 # as degree (camera module 2)
        self.y_fow_degree = 48.8 # as degree (camera module 2)
        self.x_angle_theta = 0 # as degree
        self.y_angle_theta = 0 # as degree
        self.px_to_m_x1 = 0 # as meter/px
        self.px_to_m_x2 = 0 # as meter/px
        self.px_to_m_y1 = 0 # as meter/px
        self.px_to_m_y2 = 0 # as meter/px
        self.real_distance_on_x = 0 # as meter
        self.real_distance_on_y = 0 # as meter

    @staticmethod
    def seen_distance_calculator(fow_degree, angle_theta, height):

        cos_fow_minus_theta = cos(radians(fow_degree - angle_theta))
        cos_fow_plus_theta = cos(radians(fow_degree + angle_theta))
        cos_theta = cos(radians(angle_theta))
        cos_fow = cos(radians(fow_degree))
        first_term_big = height / cos_fow_plus_theta
        second_term_big = height / cos_theta
        third_term_big = (2*(height^2)*cos_fow) / (cos_theta*cos_fow_plus_theta)
        first_term_small = height / cos_fow_minus_theta
        second_term_small = height / cos_theta
        third_term_small= (2*(height^2)*cos_fow) / (cos_theta*cos_fow_minus_theta)

        distance_big_squared =  first_term_big**2 + second_term_big**2 + third_term_big
        distance_big = sqrt(distance_big_squared)

        distance_small_squared =  first_term_small**2 + second_term_small**2 + third_term_small
        distance_small = sqrt(distance_small_squared)
        
        return distance_big, distance_small
    
    # TODO check if "=" signs cause any error
    def find_region_update(self):
        if self.distance_px_x>=0 and self.distance_px_y>=0:
            self.region = 1
        elif self.distance_px_x<0 and self.distance_px_y>0:
            self.region = 2
        elif self.distance_px_x<=0 and self.distance_px_y<=0:
            self.region = 3
        elif self.distance_px_x>0 and self.distance_px_y<0:
            self.region = 4
    
    # Hypotetically updating data from pixhawk data
    def pixhawk_update(self):
        self.height = self.height
        self.x_angle_theta = self.x_angle_theta
        self.y_angle_theta = self.y_angle_theta

    # Needs to be updated every frame after pixhawk update as the values will change by the change of the height and theta
    def px_to_m_update(self):
        self.x1_max_distance, self.x2_max_distance = Distance.seen_distance_calculator(self.x_fow_degree, self.x_angle_theta, self.height)
        self.y1_max_distance, self.y2_max_distance = Distance.seen_distance_calculator(self.y_fow_degree, self.y_angle_theta, self.height)
        self.px_to_m_x1 = self.x1_max_distance / (self.width_px/2) # big
        self.px_to_m_x2 = self.x2_max_distance / (self.width_px/2) # small
        self.px_to_m_y1 = self.y1_max_distance / (self.height_px/2) # big
        self.px_to_m_y2 = self.y2_max_distance / (self.height_px/2) # small

    # Calculates the distance between the center of the frame and the center of the given contour
    # returns distance and x and y coordinates of the distance as one may need them seperately to calculate real distance
    def distance_px_from_contours_update(self,x_min,y_min,x_max,y_max):
        x = (x_min + x_max)/2
        y = (y_min + y_max)/2
        center_x = self.width_px/2
        center_y = self.height_px/2
        self.distance_px_x = x - center_x
        self.distance_px_y = y - center_y

    def real_distance_find_update(self):
        if self.region == 1:
            self.real_distance_on_x = self.distance_px_x * self.px_to_m_x2
            self.real_distance_on_y = self.distance_px_y * self.px_to_m_y2
        elif self.region == 2:
            self.real_distance_on_x = self.distance_px_x * self.px_to_m_x1
            self.real_distance_on_y = self.distance_px_y * self.px_to_m_y2
        elif self.region == 3:
            self.real_distance_on_x = self.distance_px_x * self.px_to_m_x1
            self.real_distance_on_y = self.distance_px_y * self.px_to_m_y1
        elif self.region == 4:
            self.real_distance_on_x = self.distance_px_x * self.px_to_m_x2
            self.real_distance_on_y = self.distance_px_y * self.px_to_m_y1
         

    # self.height, self.x_angle_theta, self.y_angle_theta should be updated for each frame, these values will be taken from pixhawk
    def main(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                self.pixhawk_update()
                self.px_to_m_update()
                self.distance_px_from_contours_update(480,480,360,360)
                self.find_region_update()
                self.real_distance_find_update()
                print(self.real_distance_on_x, self.real_distance_on_y)
                cv.imshow("sex",frame)
            if cv.waitKey(10) == ord("q"):
                break

if __name__ == "__main__":
    x = Distance(25)
    x.main()