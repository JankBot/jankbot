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
    chessboard_w = 40
    pad_x = (rw - chessboard_w) / 2
    pad_y = rh - (h / w * (rw - 2*pad_x))

    dest = np.array([[pad_x,pad_y], [rw-pad_x, pad_y], [pad_x, rh], [rw-pad_x, rh]], dtype='float32')

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
    # cv2.imshow("bird", bird)
    # cv2.imshow("bird2", birdseye(calib, trans))

    yuv = cv2.cvtColor(bird, cv2.COLOR_BGR2YUV)
    [y, u, v] = cv2.split(yuv)
    # cv2.imshow("u", u)

    ret, thresh = cv2.threshold(u, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow("thresh", thresh)

    kernel = np.array([[-1, -1, 2, 2, -1, -1]], np.float32)
    filtered = cv2.filter2D(u, -1, kernel)
    # cv2.imshow("filtered", filtered)


    cv2.waitKey(0)
    cv2.destroyAllWindows()
