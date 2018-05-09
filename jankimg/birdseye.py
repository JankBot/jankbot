import cv2
import numpy as np
import sys
import math

from .undistort import undistort


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
    chessboard_w = 35
    pad_x = (rw - chessboard_w) / 2
    pad_y = rh - (h / w * (rw - 2*pad_x))

    dest = np.array([[pad_x,pad_y], [rw-pad_x, pad_y], [pad_x, rh], [rw-pad_x, rh]], dtype='float32')

    return cv2.getPerspectiveTransform(corners, dest)


def birdseye(img, transform):
    return cv2.warpPerspective(img, transform, RESOLUTION)


def u_channel(img):
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    [y, u, v] = cv2.split(yuv)
    return u


def sobel(img):
    kernel = np.array([
        # [-1, -1, -1, 2, 2, 2, -1, -1, -1],
        # [-1, -1, -1, 2, 2, 2, -1, -1, -1],
        # [-1, -1, -1, 2, 2, 2, -1, -1, -1],
        [-1, -1, 2, 2, -1, -1],
        [-1, -1, 2, 2, -1, -1],
        [-1, -1, 2, 2, -1, -1],
    ], np.float32)
    return cv2.filter2D(img, -1, kernel)


def threshold(img):
    ret, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    return thresh


def detect_lines(img):
    lines = cv2.HoughLinesP(img, 1, math.pi/180, 10, minLineLength=3)
    if lines is None:
        return [], [0, 0, 0]
    line_x, line_y = [], []
    for [[x1, y1, x2, y2]] in lines:
        line_x.extend((x1 - RESOLUTION[0]/2, x2 - RESOLUTION[0]/2))
        line_y.extend((RESOLUTION[1] - y1, RESOLUTION[1] - y2))

    line_coeff = np.polyfit(line_y, line_x, 2)

    return lines, line_coeff


def debug_lines(img, lines):
    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)


def debug_curve(img, line_coeff):
    cv2.putText(img, str(line_coeff), (10, RESOLUTION[1]-10), cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 0, 255))
    p = np.poly1d(line_coeff)
    for n in range(0, 480, 10):
        x, y = p(n) + RESOLUTION[0]/2, RESOLUTION[1] - n
        cv2.circle(img, (int(x),y), 3, (0, 0, 255))


def img_test(path):
    test = undistort(cv2.imread(path))
    bird = birdseye(test, trans)
    # cv2.imshow("capture", test)
    # cv2.imshow("bird", bird)
    # cv2.imshow("calib", calib)
    # cv2.imshow("calib bird", birdseye(calib, trans))

    u = u_channel(bird)
    # cv2.imshow("u", u)

    filtered = sobel(u)
    # cv2.imshow("filtered", filtered)

    thresh = threshold(filtered)
    # cv2.imshow("thresh", thresh)

    # line_img = np.zeros((*RESOLUTION[::-1], 3), np.uint8)
    line_img = bird

    lines, line_coeff = detect_lines(thresh)
    p = np.poly1d(line_coeff)
    print("line:", p)
    print("curvature: {}, slope: {}, offset: {}".format(*line_coeff))

    if len(lines) != 0:
        debug_lines(line_img, lines)
        debug_curve(line_img, line_coeff)

    cv2.imshow(path, line_img)
    # cv2.imwrite('output/lines{}.png'.format(n), line_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':

    calib = undistort(cv2.imread('photoset/capture0.jpg'))

    trans = birdseye_transform(calib)

    for path in sys.argv[1:]:
        img_test(path)

