#!/usr/bin/env python3

from picamera import PiCamera

camera = PiCamera()

if __name__ == '__main__':
    for n in range(10):
        with open('test{}.jpg'.format(n), 'wb') as img:
            camera.capture(img)

