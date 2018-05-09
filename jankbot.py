#!/usr/bin/env python3

import config
from camera import Camera
from platform import Controller, car

if __name__ == '__main__':
    cam = Camera(config.CALIB_IMG)
    controller = Controller(car, cam)

    while True:
        controller.step()

