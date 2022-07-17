import numpy as np
import cv2
import glob
import argparse

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def calibrate(square_size, width=9, height=6):
    
    
    objp = np.zeros((height*width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    objp = objp * square_size

    
    objpoints = []  
    imgpoints = []  


    for i in range(1,20):
        img = cv2.imread("f"+str(i)+".png")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        
        if ret:

            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)
            
            cv2.imwrite("sex"+str(i)+".png", img)
            
            
           
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return [ret, mtx, dist, rvecs, tvecs]



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Camera calibration')
    
    parser.add_argument('--square_size', type=float, required=False, help='chessboard square size')
    
    

    args = parser.parse_args()
    ret, mtx, dist, rvecs, tvecs = calibrate(args.square_size)
    print("ret : " , ret)
    print("mtx : " , mtx)
    print("dist : ", dist)
    print("rvecs : ", rvecs)
    print("tvecs : ", tvecs)
    print("Calibration is finished. RMS: ", ret)



