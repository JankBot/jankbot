import cv2
import numpy as np
import sys
import os
import glob

assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'

# DIM=(1280, 1024)
# K=np.array([[664.7580862122838, 0.0, 606.4719822771807], [0.0, 666.1416522584125, 415.5307728077916], [0.0, 0.0, 1.0]])
# D=np.array([[-0.031602480970425936], [0.01001730945822753], [-0.020864377026039143], [0.00831768756871317]])
DIM=(720, 480)
# K=np.array([[345.0, 0.0, 345.0], [0.0, 345.0, 190.0], [0.0, 0.0, 1.0]])
# D=np.array([[0.0], [0.0], [0.0], [0.0]])
K=np.array([[347.0464967569512, 0.0, 345.6381028423219], [0.0, 349.23483039090365, 193.6250314050006], [0.0, 0.0, 1.0]])
D=np.array([[-0.03483461030252116], [0.0029723614826183634], [-0.004590284238468527], [0.0008656745800786099]])


def undistort(img_path, balance=0.2, dim2=None, dim3=None):
    img = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)