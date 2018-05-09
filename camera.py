import numpy as np
import cv2
from imutils.video.pivideostream import PiVideoStream

from jankimg.birdseye import *


class Camera(object):
    def __init__(self, calib_img, resolution, framerate):
        self.stream = PiVideoStream(resolution=resolution, framerate=framerate)
        self.transform = birdseye_transform(cv2.imread(calib_img))

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def get_line(self):
        frame = self.stream.read()
        test = undistort(frame)
        bird = birdseye(test, transform=self.transform)

        u = u_channel(bird)

        filtered = sobel(u)

        thresh = threshold(filtered)

        lines, line_coeff = detect_lines(thresh)
        # print("line:", p)
        # print("curvature: {}, slope: {}, offset: {}".format(*line_coeff))
        return line_coeff

