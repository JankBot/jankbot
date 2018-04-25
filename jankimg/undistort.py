import cv2
import numpy as np
import sys

assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'


# from: https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0


# found using other calibrate.py
DIM=(720, 480)
K=np.array([[347.0464967569512, 0.0, 345.6381028423219], [0.0, 349.23483039090365, 193.6250314050006], [0.0, 0.0, 1.0]])
D=np.array([[-0.03483461030252116], [0.0029723614826183634], [-0.004590284238468527], [0.0008656745800786099]])

map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)


def undistort(img):
    return cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        img = undistort(cv2.imread(p))
        cv2.imshow("undistorted", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

