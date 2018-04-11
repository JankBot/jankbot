#!/usr/bin/env python3

from picamera import PiCamera

camera = PiCamera()
camera.resolution = (720, 480)

if __name__ == '__main__':
    n = 0
    while True:
        input('waiting for input...')
        with open('capture{}.jpg'.format(n), 'wb') as img:
            camera.capture(img)
        print('*shutter noise*')
        n += 1

