#!/usr/bin/env python3

import time

import config
from camera import Camera
from platform import Controller, car

if __name__ == '__main__':
    cam = Camera(config.CALIB_IMG, config.IMG_RESOLUTION, config.FRAME_RATE)
    controller = Controller(car, cam)

    try:
        cam.start()
        time.sleep(2.0)
        while True:
            controller.step()
    except KeyboardInterrupt:
        cam.stop()

