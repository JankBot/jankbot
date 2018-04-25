import cv2
import numpy as np
import sys
import math


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
    # cv2.imshow("thresh", thresh)

    kernel = np.array([
        [-1, -1, 2, 2, -1, -1],
        [-1, -1, 2, 2, -1, -1],
    ], np.float32)
    filtered = cv2.filter2D(thresh, -1, kernel)
    # cv2.imshow("filtered", filtered)

    lines = cv2.HoughLinesP(filtered, 1, math.pi/180, 10, minLineLength=20)
    line_img = np.zeros((*RESOLUTION[::-1], 3), np.uint8)
    line_x, line_y = [], []
    for [[x1, y1, x2, y2]] in lines:
        line_x.extend((x1 - RESOLUTION[0]/2, x2 - RESOLUTION[0]/2))
        line_y.extend((RESOLUTION[1] - y1, RESOLUTION[1] - y2))
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    line_coeff = np.polyfit(line_y, line_x, 2)
    p = np.poly1d(line_coeff)
    print("line:", p)
    print("curvature: {}, slope: {}, offset: {}".format(*line_coeff))

    for n in range(0, 480, 10):
        x, y = p(n) + RESOLUTION[0]/2, RESOLUTION[1] - n
        cv2.circle(line_img, (int(x),y), 3, (0, 0, 255))
    cv2.imshow("line_img", line_img)


    cv2.waitKey(0)
    cv2.destroyAllWindows()
