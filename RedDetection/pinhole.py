from math import tan
class PinholeCalc:
    @staticmethod
    def distcalc(px_distance, focal_lenght, height, focal_as_px =True, fow=90):
        if focal_as_px:
            desired_distance = px_distance*height/focal_lenght
        else:
            foc_mm_to_px = px_distance / (focal_lenght*tan(fow/2))
            desired_distance = px_distance*height/(focal_lenght*foc_mm_to_px)
        return desired_distance
    @staticmethod
    def distcalcbothaxis(px_distance, focal_lenght, height, focal_as_px =True, fow=(90,90)):
        if focal_as_px:
            desired_x = px_distance[0]*height/focal_lenght[0]
            desired_y = px_distance[1]*height/focal_lenght[1]
        else:
            foc_mm_to_px_x = px_distance[0] / (focal_lenght[0]*tan(fow[0]/2))
            desired_x = px_distance[0]*height/(focal_lenght[0]*foc_mm_to_px_x)
            foc_mm_to_px_y = px_distance[1] / (focal_lenght[1]*tan(fow[1]/2))
            desired_y = px_distance[1]*height/(focal_lenght[1]*foc_mm_to_px_y)
        return desired_x, desired_y
