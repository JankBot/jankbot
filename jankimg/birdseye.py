import cv2
import numpy as np
import sys


RESOLUTION = (720, 480)
CHECKERBOARD = (7,5)


def birdseye_transform(img):
    ret, corners = cv2.findChessboardCorners(img, CHECKERBOARD)
    cv2.drawChessboardCorners(img, CHECKERBOARD, corners, ret)

    w, h = CHECKERBOARD
    corners = np.array([corners[0][0], corners[w-1][0], corners[-w][0], corners[-1][0]], dtype='float32')

    for corner in corners:
        cv2.circle(img, tuple(corner), 5, (255, 255, 255), -1)


    rw, rh = RESOLUTION
    p = 200

    dest = np.array([[p,2*p], [rw-p, 2*p], [p, rh], [rw-p, rh]], dtype='float32')

    return cv2.getPerspectiveTransform(corners, dest)


def birdseye(img, transform):
    return cv2.warpPerspective(img, transform, RESOLUTION)


if __name__ == '__main__':
    from undistort import undistort

    calib = undistort(cv2.imread('photoset/capture0.jpg'))
    test = undistort(cv2.imread('photoset/capture12.jpg'))

    trans = birdseye_transform(calib)

    bird = birdseye(test, trans)
    cv2.imshow("capture", test)
    cv2.imshow("bird", bird)
    cv2.imshow("bird2", birdseye(calib, trans))

    cv2.waitKey(0)
    cv2.destroyAllWindows()
