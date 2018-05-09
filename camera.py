import numpy as np
import cv2

from jankimg.birdseye import *

cap = cv2.VideoCapture(0)


class Camera(object):
    def __init__(self, calib_img, cap=cap):
        self.cap = cap
        self.transform = birdseye_transform(cv2.imread(calib_img))

    def get_line(self):
        ret, frame = self.cap.read()
        test = undistort(frame)
        bird = birdseye(test, transform=self.transform)

        u = u_channel(bird)

        filtered = sobel(u)

        thresh = threshold(filtered)

        lines, line_coeff = detect_lines(thresh)
        # print("line:", p)
        # print("curvature: {}, slope: {}, offset: {}".format(*line_coeff))
        return line_coeff


