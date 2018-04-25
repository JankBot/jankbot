import cv2
import numpy as np
import os
import glob

assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'


img = cv2.imread("testimg/test0.jpg", cv2.IMREAD_COLOR)

yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
[y, u, v] = cv2.split(yuv)

# TODO: perspective transform:
#       https://nikolasent.github.io/opencv/2017/05/07/Bird's-Eye-View-Transformation.html
#       https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0
#       https://chatbotslife.com/self-driving-cars-advanced-computer-vision-with-opencv-finding-lane-lines-488a411b2c3d

# andy sloane cycloid kernel
# this needs a rather small resolution???
kernel = np.array([[-1, -1, 2, 2, -1, -1]], np.float32)
filtered = cv2.filter2D(u, -1, kernel)

if __name__ == '__main__':
    cv2.imshow('input', img)
    cv2.imshow('u', u)
    cv2.imshow('filtered', filtered)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
